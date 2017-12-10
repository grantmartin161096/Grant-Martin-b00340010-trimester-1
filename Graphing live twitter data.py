import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import time

# import matplotlib allows me to present the live Twitter data in the form of and line graph, measuring the sentiment of the tweets
#
# style 'ggplot' just makes the graph look better and pleasing to the eye

style.use("ggplot")

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

# the pullData is the data I will use to construct the graph
# The pullData I will be using is the 'twitter-out.txt' file I created in the last piece of code
# lines equal to pullData split by new line
# 'xar' X array equals empty list
# 'yar' Y array equals empty list
# The line of code 'for l (line) in lines [-200:]:' is saving the graph data when it reaches 200 tweets
# The function below is constructing the graph
# x=0 and y=o are the starting points of the graph
# If the tweet is positive y = plus one and if the tweet is negative y= minus 1

def animate(i):
    pullData = open("twitter-out.txt", "r").read()
    lines = pullData.split('\n')

    xar = []
    yar = []

    x = 0
    y = 0

    for l in lines[-200:]:
        x += 1
        if "pos" in l:
            y += 1
        elif "neg" in l:
            y -= 1

        xar.append(x)
        yar.append(y)

    ax1.clear()
    ax1.plot(xar, yar)


ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()

# Reference for the code used:https://pythonprogramming.net/graph-live-twitter-sentiment-nltk-tutorial/