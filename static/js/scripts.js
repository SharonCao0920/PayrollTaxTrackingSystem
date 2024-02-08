$("form[name=signup_form").submit(function(e) {

  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/user/signup",
    type: "POST",
    data: data,
    dataType: "json",
    success: function(resp) {
      window.location.href = "/";
    },
    error: function(resp) {
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
    }
  });

  e.preventDefault();
});

$("form[name=login_form").submit(function(e) {

  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/user/login",
    type: "POST",
    data: data,
    dataType: "json",
    success: function(resp) {
      window.location.href = "/dashboard/";
    },
    error: function(resp) {
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
    }
  });

  e.preventDefault();
});

$("form[name=forgetpassword_form").submit(function(e) {

  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/user/forgetPass",
    type: "POST",
    data: data,
    dataType: "json",
    success: function(resp) {
      window.location.href = "/goresetPass/";
    },
    error: function(resp) {
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
    }
  });

  e.preventDefault();
});

$("form[name=reset_password_form").submit(function(e) {

  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/user/resetPass",
    type: "POST",
    data: data,
    dataType: "json",
    success: function(resp) {
        window.location.href = "/";
    },
    error: function(resp) {
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
    }
  });

  e.preventDefault();
});

document.addEventListener("DOMContentLoaded", function() {
  var servicesTab = document.getElementById('services-tab');
  var servicesDropdown = servicesTab.querySelector('.services-dropdown');

  // Function to check if an element is a descendant of another element
  function isDescendant(parent, child) {
      var node = child.parentNode;
      while (node != null) {
          if (node == parent) {
              return true;
          }
          node = node.parentNode;
      }
      return false;
  }

  // Show services dropdown when mouse enters services tab or its dropdown
  servicesTab.addEventListener('mouseenter', function(event) {
      servicesDropdown.classList.add('show');
  });

  // Keep showing services dropdown when mouse moves over services tab or its dropdown
  servicesTab.addEventListener('mousemove', function(event) {
      if (!isDescendant(servicesTab, event.target) && !isDescendant(servicesDropdown, event.target)) {
          servicesDropdown.classList.remove('show');
      }
  });

  // Hide services dropdown when mouse leaves services tab or its dropdown
  servicesTab.addEventListener('mouseleave', function(event) {
      if (!isDescendant(servicesTab, event.relatedTarget) && !isDescendant(servicesDropdown, event.relatedTarget)) {
          servicesDropdown.classList.remove('show');
      }
  });

  // Keep showing services dropdown when mouse moves over dropdown
  servicesDropdown.addEventListener('mousemove', function(event) {
      if (!isDescendant(servicesDropdown, event.target)) {
          servicesDropdown.classList.remove('show');
      }
  });
});
