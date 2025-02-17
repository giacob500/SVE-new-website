from flask import Flask, request, render_template

app = Flask(__name__)

# Available tags
AVAILABLE_TAGS = ["2", "3", "4"]

@app.route('/collections')
def collections():
    # Get active tags from URL
    active_tags = request.args.getlist("active_tag")

    # If all tags are selected or no tag is selected, show everything
    if set(active_tags) == set(AVAILABLE_TAGS) or not active_tags:
        active_tags = AVAILABLE_TAGS  # Show all by default

    return render_template("collections.html", active_tags=active_tags, available_tags=AVAILABLE_TAGS)

if __name__ == '__main__':
    app.run(debug=True)
