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
      window.location.href = "/gologin/";
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
      window.location.href = "/generate/";
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
        window.location.href = "/gologin/";
    },
    error: function(resp) {
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
    }
  });

  e.preventDefault();
});

$(document).ready(function() {
  let monitorUrl = null;
  $('#urlForm').submit(function(e) {
      e.preventDefault();
      monitorUrl = $('#url').val();
      $('#messages').append('<p>Monitoring ' + monitorUrl + '</p>');
      // Start monitoring
      setInterval(function() {
          if (monitorUrl) {
              $.ajax({
                  url: '/check_updates',
                  type: 'POST',
                  contentType: 'application/json',
                  dataType: 'json',
                  data: JSON.stringify({ "url": monitorUrl }),
                  success: function(response) {
                      $('#messages').append('<p>' + response.message + '</p>');
                      if (response.changes) {
                          $('#changes').html('<pre>' + response.changes + '</pre>');
                      }
                  },
                  error: function(xhr, status, error) {
                      $('#messages').append('<p>Error: ' + error + '</p>');
                  }
              });
          }
      }, 10000); // 10 seconds
  });
});

document.addEventListener("DOMContentLoaded", function() {
  function fetchData() {
      fetch("/update")
          .then(response => response.json())
          .then(data => {
              document.getElementById('status').textContent = data.message;
              document.getElementById('updates').textContent = data.update || "No updates detected.";
          })
          .catch(error => console.error('Error fetching updates:', error));
  }

  setInterval(fetchData, 10000); // Fetch updates every 10 seconds
  fetchData(); // Initial fetch
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

/* Francis: OTP */


// OTP Generation and varification script starts here 

let isOTPGenerated = false; // Declare a global boolean variable

document.getElementById('otpForm').addEventListener('submit', async function(event) {
  event.preventDefault(); 

  const email = document.getElementById('email').value.trim();

  const url =  '/generateOTP/generate-otp'

  // Data to send
  const data = {
      email: email
  };

  // Fetch request
  try {
      const response = await fetch(url, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
      });

      if (!response.ok) {
          throw new Error('Failed to generate OTP');
      }

      const responseData = await response.json();
      console.log(responseData); // Log response data
      alert('OTP generated successfully!'); // Display success message
      isOTPGenerated = true; // Set the boolean variable to true after success
      toggleOTPDivVisibility(); // Call the function to toggle div visibility
  } catch (error) {
      console.error('Error generating OTP:', error);
      alert('Failed to generate OTP'); // Display error message
  }
});

// OTP generation ends here 

// Hide / show OTP verification input 
function toggleOTPDivVisibility() {
    const otpDiv = document.getElementById("otpDiv");
    otpDiv.style.display = isOTPGenerated ? "block" : "none";
}

// OTP verification Script starts here 
document.getElementById('otpVerifyForm').addEventListener('submit', async function(event) {
  event.preventDefault(); // Prevent the default form submission

  const otp = document.getElementById('otp').value.trim();

  // URL endpoint for OTP verification
  const url = '/generateOTP/verify-otp';

  // Data to send
  const data = {
      otp: otp
  };

  // Fetch request
  try {
      const response = await fetch(url, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
      });

      if (!response.ok) {
          throw new Error('Failed to verify OTP');
      }

      const responseData = await response.json();
      if (responseData.status === "ok") {
          // implement redirect to success page 
          alert('OTP verification successful!'); // Display success message
          window.location.href = '/goresetPass/';

      } else if (responseData.status === "expired") {
          alert('OTP has expired.'); // Display error message
      } else if (responseData.status === "not found") {
          alert('OTP not found.'); // Display error message
      } else {
          alert('Unknown error occurred.'); // Display error message
      }
  } catch (error) {
      console.error('Error verifying OTP:', error);
      alert('Failed to verify OTP'); // Display error message
  }
});
// OTP verification ends here 
// OTP generation and verification scripts ends here 