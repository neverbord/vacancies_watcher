def sort_out(new_items, old_items):
    return {
        'old': [i for i in old_items if i not in new_items],
        'new': [i for i in new_items if i not in old_items],
        'same': [i for i in new_items if i in old_items]
    }