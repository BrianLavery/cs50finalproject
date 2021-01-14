from flask import Flask, render_template

def index():
    return render_template("index.html")

def numbers(a):
    ans = 2 * a
    return ans