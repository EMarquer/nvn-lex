"""View of the editor for the Novan lexical network."""
from tkinter import *
from tkinter import ttk
import typing as t
from ctrl.editor import VerbEditorController, PRIME_TYPES

def setup_verb_ui(content, controller: VerbEditorController):
    """Setups the user interface elements of the editor.

    Parameters:
        content: Content frame.
        controller: Editor controller, handeling interractions with the model.
    """
    # left UI: notebook and useful buttons
    left_ui = ttk.Frame(content)
    left_ui.grid(sticky='nsew', row=1, column=0)
    left_ui.rowconfigure(0, weight=1)
    left_ui.columnconfigure(0, weight=1)
    left_ui.columnconfigure(1, weight=1)
    left_ui.columnconfigure(2, weight=1)
    # notebook
    tabs = ttk.Notebook(left_ui)
    tabs.grid(sticky='nsew', row=0, columnspan=3)
    tab_edit = ttk.Frame(tabs)
    tab_relate = ttk.Frame(tabs)
    tab_statistics = ttk.Frame(tabs)
    tabs.add(tab_edit, text="Edit Verb")
    setup_verb_edit_ui(tab_edit, controller)
    tabs.add(tab_relate, text="Relate Verbs")
    tabs.add(tab_statistics, text="Statistics")
    # buttons
    button_new = ttk.Button(left_ui, text="New Verb", command=controller.create_new_verb)
    button_remove = ttk.Button(left_ui, text="Remove Verb", command=controller.remove_verb)
    button_save = ttk.Button(left_ui, text="Save", command=controller.save)
    button_new.grid(sticky='nsew', row=1, column=0)
    button_remove.grid(sticky='nsew', row=1, column=1)
    button_save.grid(sticky='nsew', row=1, column=2)
    controller.root.bind("<Control-s>", lambda x: button_save.invoke())

    # separator
    sep = ttk.Separator(content, orient=VERTICAL)
    sep.grid(sticky='ns', row=1, column=1)

    # right UI: searchbar + list
    right_ui = ttk.Frame(content)
    right_ui.grid(sticky='nsew', row=1, column=2)
    setup_verb_search_ui(right_ui, controller)
    # list
    var_list_verbs = controller.var_list_verbs
    list_verbs = Listbox(right_ui, height=10, listvariable=var_list_verbs)
    list_verbs.bind("<<ListboxSelect>>", controller.select)
    list_verbs.grid(sticky='nsew', row=2, columnspan=2)
    controller.list_verbs = list_verbs
    scrollbar = ttk.Scrollbar(right_ui, orient=VERTICAL, command=list_verbs.yview)
    list_verbs.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(sticky='nse', row=2, column=2)

def setup_verb_search_ui(right_ui: ttk.Frame, controller: VerbEditorController):
    right_ui.columnconfigure(1, weight=1)
    right_ui.rowconfigure(2, weight=1)
    update_list = controller.update_verb_list

    search_ui = ttk.Labelframe(right_ui, text="Search verbs")
    search_ui.columnconfigure(0, weight=1)
    search_ui.columnconfigure(1, weight=1)
    search_ui.grid(sticky='nsew', row=1, column=0, columnspan=2)
    # searchbar -> filter list
    var_search = controller.var_search
    entry_search = ttk.Entry(search_ui, textvariable=var_search)
    entry_search.grid(sticky='nsew', row=0, columnspan=2)
    entry_search.bind("<KeyRelease>", update_list)
    # search options
    var_is_search_nvn = controller.var_is_search_nvn
    check_nvn = ttk.Radiobutton(search_ui, text="Novan", variable=var_is_search_nvn, value=True, command=update_list)
    check_en = ttk.Radiobutton(search_ui, text="English", variable=var_is_search_nvn, value=False, command=update_list)
    check_nvn.grid(sticky='ew', row=1, column=0)
    check_en.grid(sticky='ew', row=1, column=1)
    show_prime = ttk.Checkbutton(search_ui, text='Prime label', variable=controller.var_show_prime)
    show_completion = ttk.Checkbutton(search_ui, text='Completion rate', variable=controller.var_show_completion)
    show_prime["command"] = controller.update_verb_list
    show_completion["command"] = controller.update_verb_list
    show_prime.grid(sticky='ew', row=2, column=0)
    show_completion.grid(sticky='ew', row=2, column=1)

def setup_verb_edit_ui(tab_edit: ttk.Frame, controller: VerbEditorController):
    """Setups the user interface elements of the entry edition tab.

    Parameters:
        tab_edit: Content frame.
        controller: Editor controller, handeling interractions with the model.
    """
    tab_edit.columnconfigure(1, weight=1)
    tab_edit.columnconfigure(2, weight=1)

    base_frame = ttk.Frame(tab_edit)
    base_frame.columnconfigure(1, weight=1)
    base_frame.grid(sticky='nsew', row=1, column=1, columnspan=2)
    # Novan
    nvn_label = ttk.Label(base_frame, text="Novan ")
    nvn = ttk.Entry(base_frame, textvariable=controller.var_nvn)
    nvn_label.grid(sticky='ew', row=0, column=0)
    nvn.grid(sticky='ew', row=0, column=1, columnspan=2)
    # Novan syllables
    nvn_syllables_label = ttk.Label(base_frame, text="Syllables ")
    nvn_syllables = ttk.Label(base_frame, textvariable=controller.var_nvn_syllables)
    nvn_play = ttk.Button(base_frame, text="Play")
    nvn_syllables_label.grid(sticky='ew', row=1, column=0)
    nvn_syllables.grid(sticky='ew', row=1, column=1)
    nvn_play.grid(sticky='ew', row=1, column=2)
    # English
    en_label = ttk.Label(base_frame, text="English ")
    en = ttk.Entry(base_frame, textvariable=controller.var_en)
    en_label.grid(sticky='ew', row=2, column=0)
    en.grid(sticky='ew', row=2, column=1, columnspan=2)

    # Checkboxes
    type_frame = ttk.Labelframe(tab_edit, text='Verb type')
    type_frame.grid(sticky='new', row=2, column=1)
    generic = ttk.Checkbutton(type_frame, text='Generic action', variable=controller.var_is_generic)
    state = ttk.Checkbutton(type_frame, text='State', variable=controller.var_is_state)
    process = ttk.Checkbutton(type_frame, text='Process', variable=controller.var_is_process)
    cognition = ttk.Checkbutton(type_frame, text='Cognition', variable=controller.var_is_cognition)
    transfer = ttk.Checkbutton(type_frame, text='Transfer', variable=controller.var_is_transfer)
    generic.grid(sticky='ew', row=1, column=0)
    state.grid(sticky='ew', row=2, column=0)
    process.grid(sticky='ew', row=3, column=0)
    cognition.grid(sticky='ew', row=4, column=0)
    transfer.grid(sticky='ew', row=5, column=0)

    # prime
    prime_frame = ttk.Labelframe(tab_edit, text='Semantic prime')
    prime_frame.grid(sticky='new', row=2, column=2)
    prime_no = ttk.Radiobutton(prime_frame, text='Not a prime', variable=controller.var_prime, value='', command=controller.update_prime)
    prime_no.grid(sticky='ew', row=1, column=0)
    for i, prime_type in enumerate(PRIME_TYPES):
        prime_type = ttk.Radiobutton(prime_frame, text=prime_type, variable=controller.var_prime, value=prime_type, command=controller.update_prime)
        prime_type.grid(sticky='ew', row=i + 2, column=0)

    # Definition
    desc_label = ttk.Labelframe(tab_edit, text='Description')
    desc_label.grid(sticky='nsew', row=3, column=1, columnspan=2)
    desc_label.columnconfigure(0, weight=1)
    desc = ttk.Panedwindow(desc_label, orient=VERTICAL)
    desc.grid(sticky='nsew')
    nvn_desc_label = ttk.Labelframe(desc, text='Novan')
    en_desc_label = ttk.Labelframe(desc, text='English')
    nvn_desc_label.grid(sticky='nsew')
    en_desc_label.grid(sticky='nsew')
    nvn_desc_label.columnconfigure(0, weight=1)
    en_desc_label.columnconfigure(0, weight=1)
    nvn_desc_label.rowconfigure(0, weight=1)
    en_desc_label.rowconfigure(0, weight=1)
    desc.add(nvn_desc_label)
    desc.add(en_desc_label)
    nvn_desc = Text(nvn_desc_label, wrap="word", height=5)
    nvn_desc.grid(sticky='nse', column=0, row=0)
    nvn_scrollbar = ttk.Scrollbar(nvn_desc_label, orient=VERTICAL, command=nvn_desc.yview)
    nvn_desc.configure(yscrollcommand=nvn_scrollbar.set)
    nvn_scrollbar.grid(sticky='nse', column=1, row=0)
    en_desc = Text(en_desc_label, wrap="word", height=5)
    en_desc.grid(sticky='nse', column=0, row=0)
    en_scrollbar = ttk.Scrollbar(en_desc_label, orient=VERTICAL, command=en_desc.yview)
    en_desc.configure(yscrollcommand=en_scrollbar.set)
    en_scrollbar.grid(sticky='nse', column=1, row=0)

    # bindings
    reg = tab_edit.register(lambda x: controller.validate_nvn_entry(nvn, x)) # Register the callback function
    nvn['validate'] = "key"
    nvn['validatecommand'] = (reg, '%P')
    nvn_play.state(['disabled']) # TODO
    for checkbutton in [generic, state, process, cognition, transfer]:
        checkbutton["command"] = controller.update_verb_type

    controller.text_nvn_desc = nvn_desc
    controller.text_en_desc = en_desc
    nvn.bind("<KeyRelease>", controller.update_nvn)
    en.bind("<KeyRelease>", controller.update_en)
    nvn_desc.bind("<KeyRelease>", controller.update_nvn_desc)
    en_desc.bind("<KeyRelease>", controller.update_en_desc)

