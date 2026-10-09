# EasyPygameWidgets

An easy-to-use UI widget library for pygame, featuring customizable buttons, sliders, text entries, screen management
and much more.

## Features

- **easy integration**: seamlessly works with existing pygame projects
- **customizable widgets**: nearly infinite styling options for colors, sounds, cursors, and more
- **screen management**: built-in screen system for creating different GUIs

## Installation

### Windows
```bash
pip install easypygamewidgets
```

### Linux/macOS
```bash
python3 -m pip install easypygamewidgets
```

## Quick Start

```python
import pygame

import easypygamewidgets as epw

pygame.init()
window = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# link the pygame window
epw.link_pygame_window(window)

# create a button
button = epw.Button(text="Click Me!")
button.place(300, 100)

# create a slider
slider = epw.Slider(text="Volume", start=0, end=100, auto_size=False, width=300)
slider.place(300, 200)

# create a text entry
entry = epw.Entry(placeholder_text="Type here...", auto_size=False, width=250)
entry.place(300, 400)


def draw():
   window.fill((30, 30, 30))


# main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # handle widget events
        epw.handle_event(event)

    # handle special widget events
    epw.handle_special_events()

    # draw all widgets
    epw.flip(draw)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
```

## Documentation

We have an [online documentation](https://easypygamewidgets.readthedocs.io/en/latest/index.html).

## Requirements

- python
- pygame (the community version pygame-ce)
- requests (for update checking in background once)

I recommend using the latest version of libraries.

## Contributing

Contributions are welcome! Please feel free to submit a pull request. Of course, you will be mentioned :)

[Contributing rules](https://github.com/PhilMunzke/easypygamewidgets?tab=contributing-ov-file)

## License

This project is licensed under the MIT License - see
the [LICENSE file](https://github.com/PhilMunzke/easypygamewidgets/blob/master/LICENSE) for details.

## Support

- Issues: [GitHub Issues](https://github.com/PhilMunzke/easypygamewidgets/issues)
- Discord: [My Account](https://www.discord.com/users/916636380967354419)
- Instagram: [My Account](https://www.instagram.com/8002_phil/)

- License: [MIT](https://github.com/PhilMunzke/easypygamewidgets/blob/master/LICENSE)
- History: [GitHub History](https://github.com/PhilMunzke/easypygamewidgets/commits/master/)

---

Made with ❤️ by Phil Munzke