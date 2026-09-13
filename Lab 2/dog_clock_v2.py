"""Paw Clock v2. --setup: choose schedules/distance; --demo: temporary demo."""
import argparse
import copy
import json
import math
import time
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / 'walk_data.json'
CONFIG_FILE = ROOT / 'dog_clock_settings.json'
STATES = ['sleep', 'awake', 'excited', 'waiting']
EXAMPLE = {'weekday': ['08:00', '14:00', '20:00'],
           'weekend': ['09:00', '15:00', '21:00'], 'distance_km': 1.0}


def write_json(path, data):
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(data, indent=2))
    tmp.replace(path)


def parse_times(value):
    result = []
    for part in value.replace('，', ',').split(','):
        hour, minute = map(int, part.strip().split(':'))
        if not (0 <= hour < 24 and 0 <= minute < 60):
            raise ValueError('Use 24-hour times, for example 08:30, 18:00')
        result.append(f'{hour:02d}:{minute:02d}')
    if not result:
        raise ValueError('Enter at least one time.')
    return sorted(set(result))


def configure():
    print('Choose your own schedule. Times use the Raspberry Pi local timezone.')
    config = {}
    for field, label in [('weekday', 'Weekdays'), ('weekend', 'Weekends')]:
        while True:
            try:
                config[field] = parse_times(input(label + ' (HH:MM, HH:MM): '))
                break
            except (ValueError, TypeError):
                print('Enter valid times, for example 08:30, 14:00, 20:00')
    while True:
        try:
            km = float(input('Estimated km per walk: '))
            if not math.isfinite(km) or km <= 0:
                raise ValueError()
            config['distance_km'] = round(km, 3)
            if config['distance_km'] <= 0:
                raise ValueError()
            break
        except ValueError:
            print('Enter a positive distance in km, for example 0.8')
    write_json(CONFIG_FILE, config)
    print('Settings saved. Saved walk distances will not change.')
    return config


def load_config():
    if not CONFIG_FILE.exists():
        return configure()
    config = json.loads(CONFIG_FILE.read_text())
    for field in ('weekday', 'weekend'):
        config[field] = parse_times(','.join(config[field]))
    km = float(config['distance_km'])
    if not math.isfinite(km) or km <= 0:
        raise ValueError('Invalid configured distance; run --setup.')
    config['distance_km'] = km
    return config


def new_data():
    return {'version': 2, 'walks': [], 'completed': [], 'skipped': [], 'snoozes': {}}


def load_data():
    if not DATA_FILE.exists():
        return new_data()
    data = json.loads(DATA_FILE.read_text())
    for field in ('walks', 'completed'):
        if not isinstance(data.get(field), list):
            raise ValueError('Invalid walk_data.json: ' + field)
    if not isinstance(data.get('snoozes'), dict):
        raise ValueError('Invalid snoozes')
    # Preserve v1 counts. Old entries have no known distance and are not guessed.
    migrated = any(isinstance(w, str) for w in data['walks'])
    for i, walk in enumerate(data['walks']):
        if isinstance(walk, str):
            data['walks'][i] = {'at': walk, 'km': None, 'slot': None}
        walk = data['walks'][i]
        datetime.fromisoformat(walk['at'])
        if walk['km'] is not None and (not math.isfinite(walk['km']) or walk['km'] < 0):
            raise ValueError('Invalid saved distance')
    data.setdefault('skipped', [])
    if not isinstance(data['skipped'], list):
        raise ValueError('Invalid skipped slots')
    for value in data['snoozes'].values():
        datetime.fromisoformat(value)
    if migrated:
        backup = DATA_FILE.with_name('walk_data_v1_backup.json')
        if not backup.exists():
            backup.write_text(DATA_FILE.read_text())
    data['version'] = 2
    return data


def next_walk(now, data, config):
    # Pending slots expire at local midnight; they are not counted as walks.
    for offset in range(8):
        day = now.date() + timedelta(days=offset)
        schedule = config['weekend' if day.weekday() >= 5 else 'weekday']
        for value in schedule:
            due = datetime.fromisoformat(day.isoformat() + 'T' + value + ':00')
            key = due.isoformat()
            if key not in data['completed'] and key not in data['skipped']:
                return key, datetime.fromisoformat(data['snoozes'].get(key, key))
    raise ValueError('No available schedule.')


def state_for(now, due):
    minutes = (due-now).total_seconds()/60
    return 'sleep' if minutes > 30 else 'awake' if minutes > 0 else 'excited' if minutes >= -15 else 'waiting'


def remember(data):
    data['undo'] = {k: copy.deepcopy(data[k]) for k in ('walks', 'completed', 'skipped', 'snoozes')}


def act(action, now, data, config):
    if action == 'undo':
        previous = data.pop('undo', None)
        if previous is None:
            return 'Nothing to undo'
        data.update(previous)
        return 'Last action undone'
    key, due = next_walk(now, data, config)
    if action == 'skip' and datetime.fromisoformat(key).date() != now.date():
        return 'No pending walk today'
    remember(data)
    if action == 'log':
        slot = key if datetime.fromisoformat(key).date() == now.date() else None
        data['walks'].append({'at': now.isoformat(), 'km': config['distance_km'], 'slot': slot})
        if slot:
            data['completed'].append(slot)
            data['snoozes'].pop(slot, None)
        return 'Walk saved. Thank you!'
    if action == 'skip':
        data['skipped'].append(key)
        data['snoozes'].pop(key, None)
        return 'Skipped; count unchanged'
    if action == 'snooze':
        data['snoozes'][key] = (max(now, due)+timedelta(minutes=30)).isoformat()
        return 'Reminder moved +30 min'
    raise ValueError(action)


def totals(data, now):
    walks = data['walks']
    return (sum(datetime.fromisoformat(w['at']).date() == now.date() for w in walks),
            sum(datetime.fromisoformat(w['at']).year == now.year for w in walks),
            sum(w['km'] for w in walks if w['km'] is not None),
            sum(w['km'] is None for w in walks))


class Button:
    """Debounce input; emit one short/long event on release."""
    def __init__(self):
        self.raw = self.stable = False
        self.changed = self.started = 0

    def update(self, pressed, tick):
        if pressed != self.raw:
            self.raw, self.changed = pressed, tick
        if self.raw != self.stable and tick - self.changed >= 0.04:
            self.stable = self.raw
            if self.stable:
                self.started = tick
            else:
                return 'long' if tick - self.started >= 1.2 else 'short'
        return None


def render(state, count, stats=False, demo=False, message='', phase=0):
    from PIL import Image, ImageDraw, ImageFont
    image = Image.new('RGB', (240, 135), {'sleep': '#18263d', 'awake': '#245044', 'excited': '#765020', 'waiting': '#613443'}[state])
    d = ImageDraw.Draw(image)
    try:
        small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 11)
        large = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)
    except OSError:
        small = large = ImageFont.load_default()
    cream, tan, dark = '#fff3d4', '#dda46c', '#49352a'
    d.text((8, 4), 'PAW CLOCK' + ('  [DEMO]' if demo else ''), font=small, fill=cream)
    d.text((183, 4), f'{count} walks', font=small, fill=cream)
    if stats:
        d.text((22, 42), 'WALKS TODAY', font=large, fill=cream)
        d.text((100, 70), str(count), font=large, fill='#a9db9c')
    else:
        # Vector shapes rendered to pixels: no image files or emoji fonts needed.
        y = 4 if state == 'excited' and phase else 0
        d.ellipse((63, 54-y, 151, 96-y), fill=tan)
        d.ellipse((118, 34-y, 173, 83-y), fill=tan)
        d.polygon([(121, 39-y), (110, 33-y), (115, 72-y), (131, 61-y)], fill=dark)
        d.ellipse((149, 59-y, 181, 79-y), fill=cream)
        d.ellipse((171, 60-y, 180, 68-y), fill=dark)
        d.rounded_rectangle((77, 83-y, 102, 100-y), radius=6, fill=cream)
        d.rounded_rectangle((132, 82-y, 151, 100-y), radius=6, fill=cream)
        if state == 'sleep':
            d.line((144, 54-y, 153, 54-y), fill=dark, width=2)
            d.text((181, 31), 'Zzz', font=large, fill=cream)
        else:
            d.ellipse((146, 49-y, 151, 56-y), fill=dark)
        d.line([(68, 69-y), (53, (90 if state == 'waiting' else 47 if phase else 61)-y)], fill=tan, width=7)
        if state == 'waiting':
            d.text((192, 36), '...', font=large, fill=cream)
        if state == 'excited':
            for x, py in [(29, 46), (204, 72)]:
                d.ellipse((x, py, x+11, py+10), fill='#a9db9c')
                for dx, dy in [(-3, -5), (3, -9), (9, -5)]:
                    d.ellipse((x+dx, py+dy, x+dx+5, py+dy+5), fill='#a9db9c')
        labels = {'sleep': 'Resting until our next walk', 'awake': 'A walk is coming soon',
                  'excited': "Let's go for a walk!", 'waiting': 'Walk overdue. Ready?'}
        d.text((8, 103), labels[state], font=small, fill=cream)
    d.rectangle((0, 119, 240, 135), fill='#284338')
    d.text((6, 121), message or 'A: log walk   B: view / hold: later', font=small, fill=cream)
    return image


MENU = [('snooze', 'Postpone 30 min'), ('skip', 'Skip pending walk'),
        ('undo', 'Undo last action'), ('cancel', 'Back')]


def frame(state, data, now, page, menu, demo, message, phase):
    from PIL import ImageDraw, ImageFont
    today, year, km, unknown = totals(data, now)
    image = render(state, today, demo=demo, phase=phase)
    d = ImageDraw.Draw(image)
    try:
        small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 11)
        large = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 18)
    except OSError:
        small = large = ImageFont.load_default()
    if page or menu is not None:
        d.rectangle((0, 23, 239, 118), fill='#182b26')
        if menu is not None:
            title, value, note = 'CORRECTIONS', MENU[menu][1], 'Hold B: cancel'
        elif page == 1:
            title, value, note = 'WALKS TODAY', str(today), now.strftime('%Y-%m-%d')
        elif page == 2:
            title, value, note = 'WALKS THIS YEAR', str(year), str(now.year)
        else:
            title, value = 'DISTANCE TOGETHER', f'{km:.2f} km'
            note = f'Estimated; {unknown} old walks excluded' if unknown else 'Estimated / all recorded walks'
        d.text((9, 28), title, font=small, fill='#fff3d4')
        d.text((9, 51), value, font=large, fill='#a9db9c')
        d.text((9, 91), note, font=small, fill='#fff3d4')
    d.rectangle((0, 119, 239, 134), fill='#284338')
    footer = 'A: choose  B: next' if menu is not None else 'A: log  B: page  Hold A: menu'
    d.text((5, 121), message or footer, font=small, fill='#fff3d4')
    return image


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--setup', action='store_true', help='Choose weekday/weekend times and estimated km')
    parser.add_argument('--demo', action='store_true', help='Temporary records; cycle states every 5 seconds')
    parser.add_argument('--basic', action='store_true', help='Display-only first iteration')
    args = parser.parse_args()
    if args.setup:
        configure()
        return
    # Ask for settings BEFORE initializing the hardware.
    config = (load_config() if CONFIG_FILE.exists() else copy.deepcopy(EXAMPLE)) if args.demo else load_config()
    data = new_data() if args.demo else load_data()
    if args.demo:
        print('DEMO: records are temporary. Example settings used if no settings file exists.')
    print('A: log. B: page. Hold A: correction menu. Hold B: postpone. Release after each press.')
    print('Local time:', datetime.now().astimezone().isoformat())
    import board
    import digitalio
    from adafruit_rgb_display import st7789
    resources = []
    spi = None
    backlight = None
    try:
        cs = digitalio.DigitalInOut(board.D5); resources.append(cs)
        dc = digitalio.DigitalInOut(board.D25); resources.append(dc)
        spi = board.SPI()
        display = st7789.ST7789(spi, cs=cs, dc=dc, rst=None, baudrate=64000000,
                               width=135, height=240, x_offset=53, y_offset=40)
        backlight = digitalio.DigitalInOut(board.D22); resources.append(backlight)
        backlight.switch_to_output(value=True)
        pins = []
        if not args.basic:
            for pin in (board.D23, board.D24):
                button = digitalio.DigitalInOut(pin); resources.append(button)
                button.switch_to_input(pull=digitalio.Pull.UP)
                pins.append(button)
        buttons = [Button(), Button()]
        page, menu = 0, None
        message, message_until = '', 0
        start = time.monotonic()
        last_log = last_frame = -100
        demo_override_until = 0
        while True:
            now, tick = datetime.now(), time.monotonic()
            for index, pin in enumerate(pins):
                event = buttons[index].update(not pin.value, tick)
                if event is None:
                    continue
                action = None
                if menu is not None:
                    if index == 1:
                        menu = None if event == 'long' else (menu + 1) % len(MENU)
                    elif event == 'short':
                        action = MENU[menu][0]
                        menu = None
                        if action == 'cancel':
                            action = None
                elif index == 0:
                    if event == 'long':
                        menu = 0
                    elif tick - last_log >= 3:
                        action = 'log'
                elif event == 'short':
                    page = (page + 1) % 4
                else:
                    action = 'snooze'
                if action:
                    # Commit only after a successful save; keep current in-memory state on failure.
                    candidate = copy.deepcopy(data)
                    result = act(action, now, candidate, config)
                    try:
                        if not args.demo:
                            write_json(DATA_FILE, candidate)
                        data = candidate
                        message = result
                        if action == 'log':
                            last_log = tick
                        demo_override_until = tick + 3
                    except OSError as error:
                        message = 'Save failed; check terminal'
                        print('Could not save:', error)
                    message_until = tick + 3
            _, due = next_walk(now, data, config)
            state = state_for(now, due)
            if args.demo:
                state = 'sleep' if tick < demo_override_until else STATES[int((tick-start)//5) % 4]
            if tick - last_frame >= .15:
                display.image(frame(state, data, now, page, menu, args.demo,
                                    message if tick < message_until else '', int(tick*2) % 2), 90)
                last_frame = tick
            time.sleep(.01)
    except KeyboardInterrupt:
        print('\nClock stopped.')
    finally:
        if backlight is not None:
            try:
                backlight.value = False
            except Exception:
                pass
        for resource in reversed(resources):
            resource.deinit()
        if spi is not None:
            spi.deinit()


if __name__ == '__main__':
    main()