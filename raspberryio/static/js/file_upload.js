/*
    Configuration of jquery file upload.

    - Load after all other JavaScript includes.
    - Call initialize_file_uploader within a closure with two arguments:
        the url for image uploads
        the url for image downloads
*/


var initialize_file_uploader = function(image_upload_url, image_download_url) {
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
                maxFileSize: 10000000 // 10 MB
            },
            {
                action: 'resize',
                maxWidth: 1440,
                maxHeight: 900
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
};
