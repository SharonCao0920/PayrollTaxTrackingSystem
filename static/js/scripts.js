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