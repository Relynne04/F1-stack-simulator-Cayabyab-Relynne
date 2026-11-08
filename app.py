"""Flask Stack Simulator (LIFO: Last In, First Out).

Run with:  python app.py   then open http://127.0.0.1:5000
"""
import os
import secrets

from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)

from stack_model import Stack

app = Flask(__name__)
# The secret key signs the session cookie and flash messages.
# This lesson uses short fictional stack values on localhost.
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or secrets.token_hex(32)

MAX_ITEMS = 20      # most values the stack may hold at one time
MAX_LENGTH = 24     # most characters allowed in one value
MAX_HISTORY = 20    # most removed values that are remembered


@app.route('/')
def index():
    stack = Stack(session.get('stack', []))
    popped = session.get('popped', [])
    # peek is a one-time flag: it is read once, then removed from the session.
    highlight = session.pop('peek', False)
    return render_template(
        'index.html',
        items=list(reversed(stack.items)),   # top of the stack is shown first
        size=stack.size(),
        popped=list(reversed(popped)),       # newest removed value first
        highlight=highlight,
    )


@app.route('/stack', methods=['POST'])
def operate():
    action = request.form.get('action', '').strip().lower()
    value = request.form.get('value', '').strip()

    stack = Stack(session.get('stack', []))
    popped = list(session.get('popped', []))

    if action == 'push':
        if not value:
            flash('Enter a value before pressing Push.', 'error')
        elif len(value) > MAX_LENGTH:
            flash(f'A value can have at most {MAX_LENGTH} characters.', 'error')
        elif stack.size() >= MAX_ITEMS:
            flash(f'The stack is full ({MAX_ITEMS} items). Pop a value first.', 'error')
        else:
            stack.push(value)
            flash(f'Pushed "{value}" onto the top of the stack.', 'success')

    elif action == 'pop':
        if stack.is_empty():
            flash('The stack is empty. There is nothing to pop.', 'error')
        else:
            removed = stack.pop()
            popped.append(removed)
            popped = popped[-MAX_HISTORY:]       # keep the most recent only
            flash(f'Popped "{removed}" from the top of the stack.', 'success')

    elif action == 'peek':
        if stack.is_empty():
            flash('The stack is empty. There is nothing to peek.', 'error')
        else:
            session['peek'] = True               # tells index() to highlight the top
            flash(f'The top value is "{stack.peek()}". It was not removed.', 'success')

    elif action == 'clear':
        stack.clear()
        popped.clear()
        flash('The stack and the removed items were cleared.', 'success')

    else:
        flash('Unknown action.', 'error')

    # Reassign so Flask notices the change and saves the session.
    session['stack'] = stack.items
    session['popped'] = popped
    return redirect(url_for('index'))


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run()  # Local development only. Stop with Ctrl+C.
