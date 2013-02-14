function CustomFileBrowser(field_name, url, type, win) {
    tinyMCE.activeEditor.windowManager.open({
        file: window.__filebrowser_url + '?pop=2&type=' + type,
        width: 820,
        height: 500,
        resizable: "yes",
        scrollbars: "yes",
        inline: "yes",  // This parameter only has an effect if you use the inlinepopups plugin!
        close_previous: "no"
    }, {
        window: win,
        input: field_name,
        editor_id: tinyMCE.selectedInstance.editorId
    });
    return false;
}

if (typeof tinyMCE != 'undefined') {

    tinyMCE.init({

        // main settings
        mode : "specific_textareas",
        editor_selector : "mceEditor",
        theme: "advanced",
        language: "en",
        dialog_type: "window",
        editor_deselector : "mceNoEditor",

        // general settings
        width: '100%',
        height: '350',
        indentation : '10px',
        fix_list_elements : true,
        relative_urls: false,
        remove_script_host : true,
        accessibility_warnings : false,
        object_resizing: true,
        //cleanup: false, // SETTING THIS TO FALSE WILL BREAK EMBEDDING YOUTUBE VIDEOS
        forced_root_block: "p",
        remove_trailing_nbsp: true,
        remove_linebreaks : true,

        // theme_advanced
        theme_advanced_toolbar_location: "top",
        theme_advanced_toolbar_align: "left",
        theme_advanced_statusbar_location: "",
        theme_advanced_buttons1: "bold,italic,|,link,unlink,|charmap,|,code,|,table,|,bullist,numlist,blockquote,|,undo,redo,",
        theme_advanced_buttons2: "",
        theme_advanced_buttons3: "",
        theme_advanced_path: false,
        //theme_advanced_blockformats: "p,h1,h2,h3,h4,pre",
        theme_advanced_resizing : true,
        theme_advanced_resize_horizontal : true,
        theme_advanced_resizing_use_cookie : true,
        advlink_styles: "intern=internal;extern=external",

        // remove MS Word's inline styles when copying and pasting.
        paste_remove_spans: true,
        paste_auto_cleanup_on_paste : true,
        paste_remove_styles: true,
        paste_remove_styles_if_webkit: true,
        paste_strip_class_attributes: true,

        setup : function(ed){
            ed.onInit.add(function(ed)
            {
                var e = ed.getBody();
                e.style.fontSize='14px';
                e.style.fontFamily='tahoma,sans-serif';
                e.style.fontWeight='normal';
            });
        }

    });

}
