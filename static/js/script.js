    $(document).ready(function() {
    let counter = 2;
    $("a#add").click(function() {
        counter++;
        $("#submit").remove();
        $("form").append(
        '<div class="person-container">' +
        '<div class="row p-2">' +
        '<div class="col-2"><h4><span class="badge bg-primary mt-2">'+counter+'</span></h4></div>' +
        '<div class="col-5">' +
        '<input type="text" name="name" class="form-control w-50 p-2 ms-5" placeholder="Name"/>' +
        '</div>' +
        '<div class="col-5">' +
        '<input type="text" name="email" class="form-control w-50 p-2 ms-5" placeholder="Email"/>' +
        '</div>' +
        '</div>' +
        '</div>' +
        '<button type="submit" class="btn btn-primary btn-lg px-4 gap-3 mt-3" id="submit">Add</button>');
        });
    $("a#remove").click(function() {
        counter--;
        $("#submit").remove();
        $("form .person-container:last-child").remove();
        $("form").append(
        '<button type="submit" class="btn btn-primary btn-lg px-4 gap-3 mt-3" id="submit">Add</button>');
        });
    });