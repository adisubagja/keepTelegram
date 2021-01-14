"""Utils for bot"""
from datetime import datetime

# ------------ Program variable start ----------- #
status_codes = {
    0: {'str': 'unready', 'reverse_str': 'ready', 'int': 1},
    1: {'str': 'ready', 'reverse_str': 'unready', 'int': 0},
}
note_fields = ['header', 'text', 'time']
buttons_text = {
    'get_text': 'Get list of available commands',
    'add_text': 'Add a new note'}
# ------------ Program variables end ------------ #


# ------------ Program functions start ---------- #
def note_template(data):
    """Create note template"""
    return f"""
<strong>Header</strong>: <i>{data[1]}</i>
<strong>Text</strong>: <i>{data[2]}</i>
<strong>Status</strong>: <i>{status_codes[data[3]].get('str')}</i>
<strong>Due time</strong>: <i>{data[4]}</i>
"""


def statistics_template(data):
    """Create statistics template"""
    return f"""
\N{memo} Number of <strong>all</strong> notes: <i>{data.get('all_num')}</i>
\N{cross mark} Number of <strong>unready</strong> notes: <i>{data.get('unready_num')}</i>
\N{check mark} Number of <strong>ready</strong> notes: <i>{data.get('ready_num')}</i>
"""


def get_time_obj(date_time_str):
    """Check if date format is correct"""
    try:
        date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')
        return date_time_obj
    except ValueError as error:
        print(f'Error: {error}')
        return None
# ------------ Program functions end ------------ #
