$(document).ready(function()
    {
        $(".follow-btn").delegate(".following", "click", function(e) {
             e.preventDefault();
             var item = $(this);
             $.post( $(this).attr("href"), function() {
                     $(item).attr('class', 'follow')
                            .text('Follow')
                            .attr('href', $(item).attr('href').replace(/following/i, "follow_all"));
                     var followers = +$('#followers').text();
                     $('#followers').text(followers - 1);
                });
          });
        $(".follow-btn").delegate(".follow", "click", function(e) {
             e.preventDefault();
             var item = $(this);
             $.post( $(this).attr("href"), function() {
                     $(item).attr('class', 'following')
                            .text('Following')
                            .attr('href', $(item).attr('href').replace(/follow_all/i, "following"));
                     var followers = +$('#followers').text();
                     $('#followers').text(followers + 1);
             });
        });
    });
