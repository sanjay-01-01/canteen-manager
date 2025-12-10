// management/static/js/daily_entry_logic.js

(function($) {
    $(document).ready(function() {
        var $canteenField = $('#id_canteen'); // Canteen Name dropdown ID

        // Fieldsets (JS इन्हें नियंत्रित करेगा)
        // आपके admin.py में fieldsets की क्रम संख्या:
        // 2nd fieldset: Daily Supply Quantities
        // 3rd fieldset: Daily Payment Received
        var $supplySection = $('.fieldset.module:nth-of-type(2)');
        var $paymentSection = $('.fieldset.module:nth-of-type(3)');
        var $teaField = $('.field-tea_qty');

        // 1. फ़ील्ड्स को दिखाने/छिपाने का लॉजिक
        function toggleFields(canteenId) {
            // चुने गए ऑप्शन से सीधे data-billing-type एट्रीब्यूट पढ़ें
            var billingType = $canteenField.find('option:selected').attr('data-billing-type');

            // शुरू में सब छिपाएँ (यदि Canteen नहीं चुनी गई है)
            $supplySection.hide(); 
            $paymentSection.hide();
            $teaField.hide(); // Tea Qty को भी छिपाएँ

            // यदि Canteen ID चुना गया है, तो लॉजिक चलाएँ
            if (canteenId && billingType) {
                $supplySection.show(); // Supply सेक्शन हमेशा दिखाओ

                if (billingType === 'DAILY') {
                    $paymentSection.show(); // Cash/Online दिखाओ
                    $teaField.show();      // Tea Qty दिखाओ
                } else if (billingType === 'MONTHLY') {
                    $paymentSection.hide(); // Cash/Online छिपाओ
                    $teaField.hide();      // Tea Qty छिपाओ (जैसा आपने मांगा)
                }
            }
        }

        // 2. Canteen ड्रॉपडाउन में बदलाव पर लॉजिक चलाएँ
        $canteenField.change(function() {
            toggleFields($(this).val());
        });

        // 3. पेज लोड होने पर फ़ील्ड्स को पहली बार सही ढंग से सेट करें
        toggleFields($canteenField.val());

        // 4. शुरू में सब छिपाएँ (CSS लोड न होने पर भी सुरक्षित रहने के लिए)
        if (!$canteenField.val()) {
             $supplySection.hide(); 
             $paymentSection.hide();
        }

    });
})(django.jQuery);