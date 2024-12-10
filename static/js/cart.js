document.addEventListener("DOMContentLoaded", function() {
	document.querySelectorAll(".delete-button").forEach(button => {
		button.addEventListener("click", function() {
			const productId = this.dataset.id;
			fetch(`/delete-item/?id=${productId}`, {
				method: 'GET',
			}).then(response => {
				if (response.ok) {
					const deletedItem = this.closest('.fadeInUp');
        			deletedItem.remove();
				} else {
					alert('Failed to delete item');
				}
			});
		});
	});
});

let time = document.getElementById("current-time");

		setInterval(() =>{
			let d = new Date();
			time.innerHTML = d.toLocaleTimeString();
		})


		var user = '{{request.user}}'

		function getToken(name) {
		    var cookieValue = null;
		    if (document.cookie && document.cookie !== '') {
		        var cookies = document.cookie.split(';');
		        for (var i = 0; i < cookies.length; i++) {
		            var cookie = cookies[i].trim();
		            // Does this cookie string begin with the name we want?
		            if (cookie.substring(0, name.length + 1) === (name + '=')) {
		                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
		                break;
		            }
		        }
		    }
		    return cookieValue;
		}
		var csrftoken = getToken('csrftoken')

		function getCookie(name) {
		    // Split cookie string and get all individual name=value pairs in an array
		    var cookieArr = document.cookie.split(";");

		    // Loop through the array elements
		    for(var i = 0; i < cookieArr.length; i++) {
		        var cookiePair = cookieArr[i].split("=");

		        /* Removing whitespace at the beginning of the cookie name
		        and compare it with the given string */
		        if(name == cookiePair[0].trim()) {
		            // Decode the cookie value and return
		            return decodeURIComponent(cookiePair[1]);
		        }
		    }

		    // Return null if not found
		    return null;
		}
		var cart = JSON.parse(getCookie('cart'))

		if (cart == undefined){
			cart = {}
			console.log('Cart Created!', cart)
			document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
		}
		console.log('Cart:', cart)




		const qrCodeContainer = document.querySelector("#qrCodeContainer");
		const qrCodeImage = document.querySelector("#qrCodeImage");
		const paymentStatus = document.querySelector("#paymentStatus");
		// Truyền giá trị từ Django template vào script JavaScript
		const cartTotal = qrCodeImage.dataset.total;
		
		function generateQRCode() {
		  if (cartTotal.length > 0) {
			const qr = new QRCode(qrCodeContainer, {
			  text: cartTotal,
			  width: 220,
			  height: 220
			});
		
			qrCodeImage.src = qr.toDataURL();
			qrCodeContainer.classList.add('show');
			setTimeout(() => {
				qrCodeContainer.classList.add('hidden');
				paymentStatus.classList.remove('hidden');
			  }, 10000); // Mã QR biến mất sau 10 giây
		  } else {
			qrCodeContainer.classList.add("error");
			setTimeout(() => {
			  qrCodeContainer.classList.remove("error");
			}, 200);
		  }
		}
		function onPaymentSuccess() {
			qrCodeContainer.classList.add('hidden');
			paymentStatus.classList.remove('hidden');
		  }
		  setTimeout(onPaymentSuccess, 10000); // Hiển thị thông báo sau 10 giây
		generateQRCode();
		
        
       
		