"""Flask Queue Simulator (FIFO: First In, First Out).

Run from inside the queue-simulator folder:
    python app.py     then open http://127.0.0.1:5001
"""
import os
import secrets

from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)

from queue_model import Queue

app = Flask(__name__)
# The secret key signs the session cookie and flash messages.
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or secrets.token_hex(32)

MAX_ITEMS = 20      # most values the queue may hold at one time
MAX_LENGTH = 24     # most characters allowed in one value
MAX_HISTORY = 20    # most removed values that are remembered


@app.route('/')
def index():
    queue = Queue(session.get('queue', []))
    removed = session.get('removed', [])
    # peek is a one-time flag: it is read once, then removed from the session.
    highlight = session.pop('peek', False)
    return render_template(
        'index.html',
        items=queue.items,                  # front first, rear last (FIFO order)
        size=queue.size(),
        front=queue.front(),
        rear=queue.rear(),
        removed=list(reversed(removed)),    # newest removed value first
        highlight=highlight,
    )


@app.route('/queue', methods=['POST'])
def operate():
    action = request.form.get('action', '').strip().lower()
    value = request.form.get('value', '').strip()

    queue = Queue(session.get('queue', []))
    removed = list(session.get('removed', []))

    if action == 'enqueue':
        if not value:
            flash('Enter a value before pressing Enqueue.', 'error')
        elif len(value) > MAX_LENGTH:
            flash(f'A value can have at most {MAX_LENGTH} characters.', 'error')
        elif queue.size() >= MAX_ITEMS:
            flash(f'The queue is full ({MAX_ITEMS} items). Dequeue a value first.', 'error')
        else:
            queue.enqueue(value)
            flash(f'Enqueued "{value}" at the rear of the queue.', 'success')

    elif action == 'dequeue':
        if queue.is_empty():
            flash('The queue is empty. There is nothing to dequeue.', 'error')
        else:
            front_value = queue.dequeue()
            removed.append(front_value)
            removed = removed[-MAX_HISTORY:]     # keep the most recent only
            flash(f'Dequeued "{front_value}" from the front of the queue.', 'success')

    elif action == 'peek':
        if queue.is_empty():
            flash('The queue is empty. There is nothing to peek.', 'error')
        else:
            session['peek'] = True               # tells index() to highlight the front
            flash(f'The front value is "{queue.peek()}". It was not removed.', 'success')

    elif action == 'clear':
        queue.clear()
        removed.clear()
        flash('The queue and the removed items were cleared.', 'success')

    else:
        flash('Unknown action.', 'error')

    # Reassign so Flask notices the change and saves the session.
    session['queue'] = queue.items
    session['removed'] = removed
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=5001)  # Port 5001 lets it run beside the stack app. Stop with Ctrl+C.
