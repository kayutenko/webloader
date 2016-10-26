$(document).ready(function() {
$('[data-toggle="popover"]').popover();

$('#add_object_button').popover({delay:{show: 500, hide: 20},
                                    animation:true,
                                    title:"Create an object",
                                    placement: 'right',
                                    trigger: "hover click",
                                    content: `Create an object that will represent an entity with attributes.
                                    E.g. a review with attributes 'Author' and 'Text'`,
                                    container:'body'
                                    }).popover('toggle');


$('#add_object_button').popover({delay:{show: 600, hide: 0}}).popover('toggle');
var objects = {objects:{}};
var current_object;
var clicked=false;
var object_created = false;

var add_object = function () {
        current_object = $("#ObjectName").val().replace(' ', '');
        objects.objects[current_object] = {};
        console.log(objects);

        $('#InitializeObject').removeClass('show').addClass('hidden');
        $('#objects').removeClass('hidden').addClass('show');
        $('#finish_parsing_btn').removeClass('hidden').addClass('show');
        $('.select_object_btn').removeClass('active');
        $('#objects').append(`
                                <button type="button" class="list-group-item btn-block select_object_btn active">`
                                    + current_object +
                                `</button>
                            `);
        $('#controll_panel').removeClass('hidden').addClass('show');
        $('.input-group').popover({delay:{show: 200, hide: 20},
                                    animation:true,
                                    title:"Create an attribute",
                                    trigger: "manual hover",
                                    placement: "right",
                                    content: "Create an attribute that will store information about the created object, e.g. 'Author'",
                                    container:'body'
                                    }).popover('toggle');
};

var insert_attribute = function(name) {
        $("#attributes").append(`
                            <div class="form-group attribute">
                            <div class="input-group">
                                <span class="input-group-btn">
                                    <button class="btn btn-secondary btn-primary remove-btn" type="button">
                                        <span class="glyphicon glyphicon-remove" aria-hidden="true"></span>
                                    </button>
                                </span>
                                <input class="form-control" type="text" value=" ` +  name + `" placeholder="Attribute" id="attr1">
                                <span class="input-group-btn">
                                    <button class="btn btn-secondary btn-primary select-btn" type="button">
                                        Select
                                    </button>
                                </span>
                            </div>
                         </div>
                         `
                        );
        if (!! clicked ) {
        $('.select-btn').popover({delay:{show: 200, hide: 20},
                                    animation:true,
                                    title:"Select elements",
                                    trigger: "manual hover",
                                    placement: "right",
                                    content: "Select elements of the page that will be stored in this attribute",
                                    container:'body'
                                    }).popover('toggle');};

};


$('#add_object_button').click(function () {

    $('#add_object_button').popover("destroy");

    $('#controll_panel').removeClass('show').addClass('hidden');
    $('.attribute').remove();
    $('#InitializeObject').removeClass('hidden').addClass('show');
});

var add_attr = function() {
    var name = $('#add_attr').val();
    objects['objects'][current_object][name] = {};
    insert_attribute(name);
         $('.remove-btn').click(function() {
            $(this).parents('.form-group').remove();
         });

         $('.select-btn').click(function () {
            if (!! clicked) {
            $('div.parser_select:nth-child(2):first').popover({delay:{show: 200, hide: 20},
                                    animation:true,
                                    title:"Click on elements",
                                    trigger: "manual hover",
                                    placement: "left",
                                    content: "Click on elements of the page that will be stored in this attribute",
                                    container:'body'
                                    }).popover('toggle');};

//            setTimeout(function() {$('div.parser_select:nth-child(2):first').popover('destroy')}, 2000);

            $('.select-btn').popover("destroy");
            var current_attribute_name = $(this).parents('.input-group-btn').siblings('.form-control').val().replace(' ', '');
            console.log('Current attribute:' + current_attribute_name);
            $(this).toggleClass('btn-warning').toggleClass('disabled').html('Done').toggleClass('selected_attr');
            var current_attribute = objects['objects'][current_attribute_name];
            $('.parser_select').addClass('on');
            $('.parser_select').click(function () {
                var clicked = true;
                $('div.parser_select:nth-child(2):first').popover('destroy');
                if ( !!clicked ) { $('.select-btn').popover({delay:{show: 200, hide: 20},
                        animation:true,
                        title:"Save selection",
                        trigger: "manual",
                        placement: "bottom",
                        container:'body'
                        }).popover('toggle');};
                var selector = '.' + $(this).children().attr('class').split(' ').join('.');
                console.log('Current selector:' +  selector);
                $('.parser_select').removeClass('active');
                $(this).toggleClass('active');
                $('.selected').removeClass('selected');
                $(selector).toggleClass('selected');

                $('.selected_attr').toggleClass('btn-warning').toggleClass('disabled').toggleClass('btn-success');

                $('.selected_attr').click(function () {
                    console.log('Current objects state:' + objects);
                    objects['objects'][current_object][current_attribute_name] = {'selector':selector};
                    console.log('Added objects' + objects);
//                    objects['objects'][current_object][current_attribute_name]['selector'] = selector;
                    console.log(objects);
                    $(this).removeClass('btn-warning').addClass('finished_attr').removeClass('disabled').html(
                                            '<span class="glyphicon glyphicon-ok-sign" aria-hidden="true"></span>');
                    $('.parser_select').removeClass('on');
                    $('.selected').removeClass('selected');
                    $('.active').removeClass('active');
                    $('#finish_parsing_btn').removeClass('btn-default').addClass('btn-success').removeClass('disabled')
                    $('.finished_attr').click(function () {
                            $(this).toggleClass('btn-warning').toggleClass('disabled').html('Done');
                        });
                });
            });
         });
    };


$('.attr-btn').click(function(){
   $('#attributes').removeClass('hidden').addClass('show');
   $('.input-group').popover("destroy");
   add_attr()
});

$('.add_object').click(function() {
    add_object();
    $(".select_object_btn").click(function () {
            current_object = $(this).html();
        $('.select_object_btn').removeClass('active');
        $(this).addClass("active")
        $('.attribute').remove();
        attributes = objects['objects'][current_object];
        Object.keys(attributes).forEach(function(key,index) {
           insert_attribute(key);
        });

    });
});
var task_id;

var polling = function (task_id) {
console.log('running polling...');
$.get('/results/' + task_id, function (data) {
    console.log(data);
  if (data.ready) {
    console.log(data['result']);
    $('.modal-body').html(`<h1>`+ data['result'] +`</h1>`);
    $('.modal').modal('show');
  } else {
    setTimeout(function () {
      polling(task_id);
    }, 1000);
  }
});
};

$('#finish_parsing_btn').click(function () {
    console.log(JSON.stringify(objects));
    $.post('/get_parsing_config', JSON.stringify(objects), function (data) {
        console.log(data['task_id']);
        polling(data['task_id']);
    })

});


});

