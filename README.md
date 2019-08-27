# GoGoRat

### AI developed for the PyRat Game, winner of the competition between AI's in 2019.
![](https://www.google.com/search?biw=1366&bih=631&tbm=isch&sa=1&ei=IP5kXeWMC4HqaN7Cn5AB&q=image+pyrat+game+telecom+bretagne&oq=image+pyrat+game+telecom+bretagne&gs_l=img.3...4381.8174..8587...0.0..0.80.995.17......0....1..gws-wiz-img.ZJY42ci_R2k&ved=0ahUKEwjlnJq15KLkAhUBNRoKHV7hBxIQ4dUDCAY&uact=5#imgrc=FzfKFOScaipSlM:)

This AI combines a Supervised Approach with a CGT (Combinatorial Game Theory) approach in order to obtain maximum performance,
not only against the greedy algorithm but also against other types of AI.The supervised learning model was trained using games of the greedy algorithm against itself, but also against a reinforcement learning algorithm trained against the greedy, in order to increase robustness.

Please cite you use this code.

In order to use this, you have to download the original PyRat Game by cloning:
[official PyRat repository](https://github.com/vgripon/pyrat)

Now you are ready to launch PyRat games.

To use this AI, you need to both gogorat: 'gogorat.py' and the supervised trained classifier in the folder AI.

After that you just have to launch the game choosing as your AI GoGoRat, like this:
#### python3 pyrat.py -p 40 -md 0 -d 0 --nonsymmetric --rat AIs/gogorat.py --python AIs/manh.py --tests 1000 --drawing --synchronous --save#





The PyRat original game the credits are available in https://github.com/vgripon. Please, follow the instructions in the same link for install the game before run the Reiforcement Learning IA.
