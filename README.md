# Drawing SVGs with Fourier Series
https://github.com/user-attachments/assets/1b359b78-c0ac-4d0b-b713-1de83f56ae59

## What is this?
The idea is that you can visualize a set of SVGs icons being drawn by the sum of N given arrows which, rotating in opposite directions and different frequencies, are set from tip to tail.

## How to use?
1. git clone
2. cd 'path_where_cloned/fourier-series-drawings'
3. py -m venv venv
4. venv\Scripts\activate
5. pip install -r requirements.txt
6. python main.py

## Controls
- Finish program: Esc
- Pause/start program: S
- Draw/not draw arrows: D
- Next/previous svg: Up/down arrow
- Divide SVG shapes in more/less points: Right/left arrow
- Add arrows/Remove arrows: Enter/tab
- Extend/contract svg: Space/backspace
- Make bigger/smaller the jump in the draw: N/M

Based on 3Blue1Brown [But what is a Fourier series? From heat flow to drawing with circles](https://www.youtube.com/watch?v=r6sGWTCMz2k)
