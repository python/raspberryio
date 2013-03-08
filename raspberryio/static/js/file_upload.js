/*
    Configuration of jquery file upload. Binds to a hidden field of a form to
    provide the image upload ids when that form is submitted

    To use, be sure to:
    1. Load after all other JavaScript includes for jQuery File Upload.

    2. Call initialize_file_uploader within a closure on the page where the
    form is used and provide 3 arguments:
        the url for image uploads
        the url for image downloads
        a jquery selector for the hidden field to submit image ids to.
*/


var initialize_file_uploader = function(
    image_upload_url, image_download_url, $file_field) {
    // Establish endpoint for uploading images
    $('#fileupload').fileupload({
        url: image_upload_url
    });

    // Enable iframe cross-domain access via redirect option:
    $('#fileupload').fileupload(
        'option',
        'redirect',
        window.location.href.replace(
            /\/[^\/]*$/,
            '/cors/result.html?%s'
        )
    );

    // Set fileupload settings
    $('#fileupload').fileupload('option', {
        url: image_upload_url,
        maxFileSize: 5000000,
        acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
        process: [
            {
                action: 'load',
                fileTypes: /^image\/(gif|jpeg|png)$/,
                maxFileSize: 5000000 // 5 MB
            },
            {
                action: 'resize',
                maxWidth: 1200,
                maxHeight: 800,
                minWidth: 800,
                minHeight: 600
            },
            {
                action: 'save'
            }
        ]
    });

    // For browsers with CORS support, reports if the server is down:
    if ($.support.cors) {
        $.ajax({
            url: image_upload_url,
            type: 'HEAD'
        }).fail(function () {
            $('<span class="alert alert-error"/>')
                .text('Upload server currently unavailable')
                .appendTo('#fileupload');
        });
    }
    
    // Load existing files into the preview section:
    if (image_download_url !== '') {
        $.ajax({
            url: image_download_url,
            dataType: 'json',
            context: $('#fileupload')[0]
        }).done(function (result) {
            foo = result;
            $(this).fileupload('option', 'done')
                .call(this, null, {result: result});
        });
    }

    /*
    When the partner form `$form` is submitted, load ids of new image uploads
    and fill the hidden file field `$file_field` with a comma separated list of
    these.
    */
    var $form = $file_field.parents('form').first();
    $form.submit(function(e) {
        var $new_uploads = $('tr.template-download td.preview');
        var image_ids = '';
        $.each($new_uploads, function(index, upload){
            var upload_id = $(upload).first().data('id');
            if (upload_id !== '') {
                if (image_ids !== '') {
                    image_ids += ',';
                }
                image_ids += upload_id;
            }
        });
        $file_field.val(image_ids);
    });
};
