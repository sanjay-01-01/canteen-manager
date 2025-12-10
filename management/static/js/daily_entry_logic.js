// management/static/js/daily_entry_logic.js

document.addEventListener('DOMContentLoaded', function() {
    const canteenSelect = document.getElementById('id_canteen');
    
    // Rows (Fieldsets के हिसाब से क्लास नाम)
    const supplyRows = document.querySelectorAll('.field-lunch_qty, .field-dinner_qty, .field-nasta_qty, .field-tea_qty');
    const paymentRows = document.querySelectorAll('.field-cash_received, .field-online_received');
    
    // नए Token Rows
    const tokenRows = document.querySelectorAll('.field-normal_token_qty, .field-special_token_qty, .field-guest_token_qty');

    // सर्वर से डेटा मंगाएं
    fetch('/management/get-canteen-data/') 
        .then(response => response.json())
        .then(CANTEEN_MAP => {
            
            function toggleFields() {
                const canteenId = canteenSelect.value;
                const billingType = CANTEEN_MAP[canteenId];

                // 1. शुरू में सबको छिपाएं
                supplyRows.forEach(el => el.style.display = 'none');
                paymentRows.forEach(el => el.style.display = 'none');
                tokenRows.forEach(el => el.style.display = 'none');

                // 2. अगर कोई कैंटीन चुनी गई है
                if (canteenId && billingType) {
                    
                    // Supply हमेशा दिखाएं
                    supplyRows.forEach(el => el.style.display = '');

                    // Payment अब हमेशा दिखाएं (चाहे DAILY हो या MONTHLY)
                    paymentRows.forEach(el => el.style.display = '');

                    // Tokens का लॉजिक (सिर्फ Monthly के लिए)
                    if (billingType === 'MONTHLY') {
                        tokenRows.forEach(el => el.style.display = ''); // दिखाएं
                    } else {
                        tokenRows.forEach(el => el.style.display = 'none'); // छिपाएं
                    }
                }
            }

            if (canteenSelect) {
                canteenSelect.addEventListener('change', toggleFields);
                toggleFields(); // पेज लोड होने पर चलाएं
            }
        })
        .catch(error => console.error('Error loading canteen data:', error));
});