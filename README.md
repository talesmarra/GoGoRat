# GoGoRat

### AI developed for the PyRat Game, winner of the competition between AI's in 2019.
![rat](https://user-images.githubusercontent.com/46964784/63762989-20be5300-c8c4-11e9-8903-bb7302067c9f.jpeg)

This AI combines a Supervised Approach with a CGT (Combinatorial Game Theory) approach in order to obtain maximum performance,
not only against the greedy algorithm but also against other types of AI.The supervised learning model was trained using games of the greedy algorithm against itself, but also against a reinforcement learning algorithm trained against the greedy, in order to increase robustness.
Achieved performance against the greedy: 72% wins.

Please cite you use this code.

In order to use this, you have to download the original PyRat Game by cloning:
[official PyRat repository](https://github.com/vgripon/pyrat)

Now you are ready to launch PyRat games.

To use this AI, you need to both gogorat: 'gogorat.py' and the supervised trained classifier in the folder AI.

After that you just have to launch the game choosing as your AI GoGoRat, like this:
#### python3 pyrat.py -p 40 -md 0 -d 0 --nonsymmetric --rat AIs/gogorat.py --python AIs/manh.py --tests 1000 --drawing --synchronous --save#





The PyRat original game the credits are available in https://github.com/vgripon. Please, follow the instructions in the same link for install the game before run the Reiforcement Learning IA.
