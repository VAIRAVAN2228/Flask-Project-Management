async function predictRevenue() {
 
    const tourists = document.querySelector('input[name="tourists"]').value;
    const temperature = document.querySelector('input[name="temperature"]').value;
    const holiday = document.querySelector('select[name="holiday"]').value;
    const event = document.querySelector('select[name="event"]').value;
 
    if (!tourists || !temperature) {
        document.getElementById("result").innerHTML = "Please fill all required fields.";
        return;
    }
 
    const data = {
        tourists: parseInt(tourists),
        temperature: parseInt(temperature),
        holiday: parseInt(holiday),
        event: parseInt(event)
    };
 
    console.log('Sending data:', data);
 
    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
 
        console.log('Response status:', response.status);
        console.log('Response content-type:', response.headers.get('content-type'));
 
        let result;
        const contentType = response.headers.get('content-type');
       
        if (contentType && contentType.includes('application/json')) {
            result = await response.json();
        } else {
            const text = await response.text();
            console.log('Response text:', text.substring(0, 200));
            result = { error: 'Invalid response format from server' };
        }
 
        console.log('Response data:', result);
 
        if (!response.ok) {
            throw new Error(result.error || `HTTP error! status: ${response.status}`);
        }
 
        if (result.error) {
            document.getElementById("result").innerHTML = "Error: " + result.error;
        } else {
            document.getElementById("result").innerHTML =
                "Predicted Revenue: ₹ " + result.predicted_revenue;
        }
    } catch (error) {
        console.error('Prediction error:', error);
        document.getElementById("result").innerHTML =
            "Error: " + error.message;
    }
}