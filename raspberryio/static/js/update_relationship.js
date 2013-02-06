$(document).ready(function()
    {
        $(".follow-btn").delegate(".unfollow", "click", function(e) {
             e.preventDefault();
             var item = $(this);
             $.post( $(this).attr("href"), function() {
                     $(item).attr('class', 'follow')
                            .text('Follow')
                            .attr('href', $(item).attr('href').replace(/remove/i, "add"));
                     var followers = +$('#followers').text();
                     $('#followers').text(followers - 1);
                });
          });
        $(".follow-btn").delegate(".follow", "click", function(e) {
             e.preventDefault();
             var item = $(this);
             $.post( $(this).attr("href"), function() {
                     $(item).attr('class', 'unfollow')
                            .text('Unfollow')
                            .attr('href', $(item).attr('href').replace(/add/i, "remove"));
                     var followers = +$('#followers').text();
                     $('#followers').text(followers + 1);
             });
        });
    });
