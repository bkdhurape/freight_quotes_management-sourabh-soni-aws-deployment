# Generated by Django 2.2.5 on 2020-11-30 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0024_invitedvendor_contact_no_dial_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='contact_no_dial_code',
            field=models.CharField(blank=True, choices=[('+376', '+376'), ('+971', '+971'), ('+93', '+93'), ('+1-268', '+1-268'), ('+1-264', '+1-264'), ('+355', '+355'), ('+374', '+374'), ('+244', '+244'), ('+672', '+672'), ('+54', '+54'), ('+1-684', '+1-684'), ('+43', '+43'), ('+61', '+61'), ('+297', '+297'), ('+358', '+358'), ('+994', '+994'), ('+387', '+387'), ('+1-246', '+1-246'), ('+880', '+880'), ('+32', '+32'), ('+226', '+226'), ('+359', '+359'), ('+973', '+973'), ('+257', '+257'), ('+229', '+229'), ('+590', '+590'), ('+1-441', '+1-441'), ('+673', '+673'), ('+591', '+591'), ('+55', '+55'), ('+1-242', '+1-242'), ('+975', '+975'), ('+47', '+47'), ('+267', '+267'), ('+375', '+375'), ('+501', '+501'), ('+1', '+1'), ('+61', '+61'), ('+243', '+243'), ('+236', '+236'), ('+242', '+242'), ('+41', '+41'), ('+225', '+225'), ('+682', '+682'), ('+56', '+56'), ('+237', '+237'), ('+86', '+86'), ('+57', '+57'), ('+506', '+506'), ('+53', '+53'), ('+238', '+238'), ('+599', '+599'), ('+61', '+61'), ('+357', '+357'), ('+420', '+420'), ('+49', '+49'), ('+253', '+253'), ('+45', '+45'), ('+1-767', '+1-767'), ('+1-809', '+1-809'), ('+213', '+213'), ('+593', '+593'), ('+372', '+372'), ('+20', '+20'), ('+212', '+212'), ('+291', '+291'), ('+34', '+34'), ('+251', '+251'), ('+358', '+358'), ('+679', '+679'), ('+500', '+500'), ('+691', '+691'), ('+298', '+298'), ('+33', '+33'), ('+241', '+241'), ('+44', '+44'), ('+1-473', '+1-473'), ('+995', '+995'), ('+594', '+594'), ('+44', '+44'), ('+233', '+233'), ('+350', '+350'), ('+299', '+299'), ('+220', '+220'), ('+224', '+224'), ('+590', '+590'), ('+240', '+240'), ('+30', '+30'), ('+500', '+500'), ('+502', '+502'), ('+1-671', '+1-671'), ('+245', '+245'), ('+592', '+592'), ('+852', '+852'), ('+672', '+672'), ('+504', '+504'), ('+385', '+385'), ('+509', '+509'), ('+36', '+36'), ('+62', '+62'), ('+353', '+353'), ('+972', '+972'), ('+44', '+44'), ('+91', '+91'), ('+246', '+246'), ('+964', '+964'), ('+98', '+98'), ('+354', '+354'), ('+39', '+39'), ('+44', '+44'), ('+1-876', '+1-876'), ('+962', '+962'), ('+81', '+81'), ('+254', '+254'), ('+996', '+996'), ('+855', '+855'), ('+686', '+686'), ('+269', '+269'), ('+1-869', '+1-869'), ('+850', '+850'), ('+82', '+82'), ('+965', '+965'), ('+1-345', '+1-345'), ('+7', '+7'), ('+856', '+856'), ('+961', '+961'), ('+1-758', '+1-758'), ('+423', '+423'), ('+94', '+94'), ('+231', '+231'), ('+266', '+266'), ('+370', '+370'), ('+352', '+352'), ('+371', '+371'), ('+218', '+218'), ('+212', '+212'), ('+377', '+377'), ('+373', '+373'), ('+382', '+382'), ('+590', '+590'), ('+261', '+261'), ('+692', '+692'), ('+389', '+389'), ('+223', '+223'), ('+95', '+95'), ('+976', '+976'), ('+853', '+853'), ('+1-670', '+1-670'), ('+596', '+596'), ('+222', '+222'), ('+1-664', '+1-664'), ('+356', '+356'), ('+230', '+230'), ('+960', '+960'), ('+265', '+265'), ('+52', '+52'), ('+60', '+60'), ('+258', '+258'), ('+264', '+264'), ('+687', '+687'), ('+227', '+227'), ('+672', '+672'), ('+234', '+234'), ('+505', '+505'), ('+31', '+31'), ('+47', '+47'), ('+977', '+977'), ('+674', '+674'), ('+683', '+683'), ('+64', '+64'), ('+968', '+968'), ('+507', '+507'), ('+51', '+51'), ('+689', '+689'), ('+675', '+675'), ('+63', '+63'), ('+92', '+92'), ('+48', '+48'), ('+508', '+508'), ('+870', '+870'), ('+1', '+1'), ('+970', '+970'), ('+351', '+351'), ('+680', '+680'), ('+595', '+595'), ('+974', '+974'), ('+262', '+262'), ('+40', '+40'), ('+381', '+381'), ('+7', '+7'), ('+250', '+250'), ('+966', '+966'), ('+677', '+677'), ('+248', '+248'), ('+249', '+249'), ('+46', '+46'), ('+65', '+65'), ('+290', '+290'), ('+386', '+386'), ('+47', '+47'), ('+421', '+421'), ('+232', '+232'), ('+378', '+378'), ('+221', '+221'), ('+252', '+252'), ('+597', '+597'), ('+211', '+211'), ('+239', '+239'), ('+503', '+503'), ('+1-721', '+1-721'), ('+963', '+963'), ('+268', '+268'), ('+1-649', '+1-649'), ('+235', '+235'), ('+262', '+262'), ('+228', '+228'), ('+66', '+66'), ('+992', '+992'), ('+690', '+690'), ('+670', '+670'), ('+993', '+993'), ('+216', '+216'), ('+676', '+676'), ('+90', '+90'), ('+1-868', '+1-868'), ('+688', '+688'), ('+886', '+886'), ('+255', '+255'), ('+380', '+380'), ('+256', '+256'), ('+1', '+1'), ('+598', '+598'), ('+998', '+998'), ('+379', '+379'), ('+1-784', '+1-784'), ('+58', '+58'), ('+1-284', '+1-284'), ('+1-340', '+1-340'), ('+84', '+84'), ('+678', '+678'), ('+681', '+681'), ('+685', '+685'), ('+383', '+383'), ('+967', '+967'), ('+262', '+262'), ('+27', '+27'), ('+260', '+260'), ('+263', '+263')], max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='landline_no_dial_code',
            field=models.CharField(blank=True, choices=[('+376', '+376'), ('+971', '+971'), ('+93', '+93'), ('+1-268', '+1-268'), ('+1-264', '+1-264'), ('+355', '+355'), ('+374', '+374'), ('+244', '+244'), ('+672', '+672'), ('+54', '+54'), ('+1-684', '+1-684'), ('+43', '+43'), ('+61', '+61'), ('+297', '+297'), ('+358', '+358'), ('+994', '+994'), ('+387', '+387'), ('+1-246', '+1-246'), ('+880', '+880'), ('+32', '+32'), ('+226', '+226'), ('+359', '+359'), ('+973', '+973'), ('+257', '+257'), ('+229', '+229'), ('+590', '+590'), ('+1-441', '+1-441'), ('+673', '+673'), ('+591', '+591'), ('+55', '+55'), ('+1-242', '+1-242'), ('+975', '+975'), ('+47', '+47'), ('+267', '+267'), ('+375', '+375'), ('+501', '+501'), ('+1', '+1'), ('+61', '+61'), ('+243', '+243'), ('+236', '+236'), ('+242', '+242'), ('+41', '+41'), ('+225', '+225'), ('+682', '+682'), ('+56', '+56'), ('+237', '+237'), ('+86', '+86'), ('+57', '+57'), ('+506', '+506'), ('+53', '+53'), ('+238', '+238'), ('+599', '+599'), ('+61', '+61'), ('+357', '+357'), ('+420', '+420'), ('+49', '+49'), ('+253', '+253'), ('+45', '+45'), ('+1-767', '+1-767'), ('+1-809', '+1-809'), ('+213', '+213'), ('+593', '+593'), ('+372', '+372'), ('+20', '+20'), ('+212', '+212'), ('+291', '+291'), ('+34', '+34'), ('+251', '+251'), ('+358', '+358'), ('+679', '+679'), ('+500', '+500'), ('+691', '+691'), ('+298', '+298'), ('+33', '+33'), ('+241', '+241'), ('+44', '+44'), ('+1-473', '+1-473'), ('+995', '+995'), ('+594', '+594'), ('+44', '+44'), ('+233', '+233'), ('+350', '+350'), ('+299', '+299'), ('+220', '+220'), ('+224', '+224'), ('+590', '+590'), ('+240', '+240'), ('+30', '+30'), ('+500', '+500'), ('+502', '+502'), ('+1-671', '+1-671'), ('+245', '+245'), ('+592', '+592'), ('+852', '+852'), ('+672', '+672'), ('+504', '+504'), ('+385', '+385'), ('+509', '+509'), ('+36', '+36'), ('+62', '+62'), ('+353', '+353'), ('+972', '+972'), ('+44', '+44'), ('+91', '+91'), ('+246', '+246'), ('+964', '+964'), ('+98', '+98'), ('+354', '+354'), ('+39', '+39'), ('+44', '+44'), ('+1-876', '+1-876'), ('+962', '+962'), ('+81', '+81'), ('+254', '+254'), ('+996', '+996'), ('+855', '+855'), ('+686', '+686'), ('+269', '+269'), ('+1-869', '+1-869'), ('+850', '+850'), ('+82', '+82'), ('+965', '+965'), ('+1-345', '+1-345'), ('+7', '+7'), ('+856', '+856'), ('+961', '+961'), ('+1-758', '+1-758'), ('+423', '+423'), ('+94', '+94'), ('+231', '+231'), ('+266', '+266'), ('+370', '+370'), ('+352', '+352'), ('+371', '+371'), ('+218', '+218'), ('+212', '+212'), ('+377', '+377'), ('+373', '+373'), ('+382', '+382'), ('+590', '+590'), ('+261', '+261'), ('+692', '+692'), ('+389', '+389'), ('+223', '+223'), ('+95', '+95'), ('+976', '+976'), ('+853', '+853'), ('+1-670', '+1-670'), ('+596', '+596'), ('+222', '+222'), ('+1-664', '+1-664'), ('+356', '+356'), ('+230', '+230'), ('+960', '+960'), ('+265', '+265'), ('+52', '+52'), ('+60', '+60'), ('+258', '+258'), ('+264', '+264'), ('+687', '+687'), ('+227', '+227'), ('+672', '+672'), ('+234', '+234'), ('+505', '+505'), ('+31', '+31'), ('+47', '+47'), ('+977', '+977'), ('+674', '+674'), ('+683', '+683'), ('+64', '+64'), ('+968', '+968'), ('+507', '+507'), ('+51', '+51'), ('+689', '+689'), ('+675', '+675'), ('+63', '+63'), ('+92', '+92'), ('+48', '+48'), ('+508', '+508'), ('+870', '+870'), ('+1', '+1'), ('+970', '+970'), ('+351', '+351'), ('+680', '+680'), ('+595', '+595'), ('+974', '+974'), ('+262', '+262'), ('+40', '+40'), ('+381', '+381'), ('+7', '+7'), ('+250', '+250'), ('+966', '+966'), ('+677', '+677'), ('+248', '+248'), ('+249', '+249'), ('+46', '+46'), ('+65', '+65'), ('+290', '+290'), ('+386', '+386'), ('+47', '+47'), ('+421', '+421'), ('+232', '+232'), ('+378', '+378'), ('+221', '+221'), ('+252', '+252'), ('+597', '+597'), ('+211', '+211'), ('+239', '+239'), ('+503', '+503'), ('+1-721', '+1-721'), ('+963', '+963'), ('+268', '+268'), ('+1-649', '+1-649'), ('+235', '+235'), ('+262', '+262'), ('+228', '+228'), ('+66', '+66'), ('+992', '+992'), ('+690', '+690'), ('+670', '+670'), ('+993', '+993'), ('+216', '+216'), ('+676', '+676'), ('+90', '+90'), ('+1-868', '+1-868'), ('+688', '+688'), ('+886', '+886'), ('+255', '+255'), ('+380', '+380'), ('+256', '+256'), ('+1', '+1'), ('+598', '+598'), ('+998', '+998'), ('+379', '+379'), ('+1-784', '+1-784'), ('+58', '+58'), ('+1-284', '+1-284'), ('+1-340', '+1-340'), ('+84', '+84'), ('+678', '+678'), ('+681', '+681'), ('+685', '+685'), ('+383', '+383'), ('+967', '+967'), ('+262', '+262'), ('+27', '+27'), ('+260', '+260'), ('+263', '+263')], max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='invitedvendor',
            name='contact_no_dial_code',
            field=models.CharField(blank=True, choices=[('+376', '+376'), ('+971', '+971'), ('+93', '+93'), ('+1-268', '+1-268'), ('+1-264', '+1-264'), ('+355', '+355'), ('+374', '+374'), ('+244', '+244'), ('+672', '+672'), ('+54', '+54'), ('+1-684', '+1-684'), ('+43', '+43'), ('+61', '+61'), ('+297', '+297'), ('+358', '+358'), ('+994', '+994'), ('+387', '+387'), ('+1-246', '+1-246'), ('+880', '+880'), ('+32', '+32'), ('+226', '+226'), ('+359', '+359'), ('+973', '+973'), ('+257', '+257'), ('+229', '+229'), ('+590', '+590'), ('+1-441', '+1-441'), ('+673', '+673'), ('+591', '+591'), ('+55', '+55'), ('+1-242', '+1-242'), ('+975', '+975'), ('+47', '+47'), ('+267', '+267'), ('+375', '+375'), ('+501', '+501'), ('+1', '+1'), ('+61', '+61'), ('+243', '+243'), ('+236', '+236'), ('+242', '+242'), ('+41', '+41'), ('+225', '+225'), ('+682', '+682'), ('+56', '+56'), ('+237', '+237'), ('+86', '+86'), ('+57', '+57'), ('+506', '+506'), ('+53', '+53'), ('+238', '+238'), ('+599', '+599'), ('+61', '+61'), ('+357', '+357'), ('+420', '+420'), ('+49', '+49'), ('+253', '+253'), ('+45', '+45'), ('+1-767', '+1-767'), ('+1-809', '+1-809'), ('+213', '+213'), ('+593', '+593'), ('+372', '+372'), ('+20', '+20'), ('+212', '+212'), ('+291', '+291'), ('+34', '+34'), ('+251', '+251'), ('+358', '+358'), ('+679', '+679'), ('+500', '+500'), ('+691', '+691'), ('+298', '+298'), ('+33', '+33'), ('+241', '+241'), ('+44', '+44'), ('+1-473', '+1-473'), ('+995', '+995'), ('+594', '+594'), ('+44', '+44'), ('+233', '+233'), ('+350', '+350'), ('+299', '+299'), ('+220', '+220'), ('+224', '+224'), ('+590', '+590'), ('+240', '+240'), ('+30', '+30'), ('+500', '+500'), ('+502', '+502'), ('+1-671', '+1-671'), ('+245', '+245'), ('+592', '+592'), ('+852', '+852'), ('+672', '+672'), ('+504', '+504'), ('+385', '+385'), ('+509', '+509'), ('+36', '+36'), ('+62', '+62'), ('+353', '+353'), ('+972', '+972'), ('+44', '+44'), ('+91', '+91'), ('+246', '+246'), ('+964', '+964'), ('+98', '+98'), ('+354', '+354'), ('+39', '+39'), ('+44', '+44'), ('+1-876', '+1-876'), ('+962', '+962'), ('+81', '+81'), ('+254', '+254'), ('+996', '+996'), ('+855', '+855'), ('+686', '+686'), ('+269', '+269'), ('+1-869', '+1-869'), ('+850', '+850'), ('+82', '+82'), ('+965', '+965'), ('+1-345', '+1-345'), ('+7', '+7'), ('+856', '+856'), ('+961', '+961'), ('+1-758', '+1-758'), ('+423', '+423'), ('+94', '+94'), ('+231', '+231'), ('+266', '+266'), ('+370', '+370'), ('+352', '+352'), ('+371', '+371'), ('+218', '+218'), ('+212', '+212'), ('+377', '+377'), ('+373', '+373'), ('+382', '+382'), ('+590', '+590'), ('+261', '+261'), ('+692', '+692'), ('+389', '+389'), ('+223', '+223'), ('+95', '+95'), ('+976', '+976'), ('+853', '+853'), ('+1-670', '+1-670'), ('+596', '+596'), ('+222', '+222'), ('+1-664', '+1-664'), ('+356', '+356'), ('+230', '+230'), ('+960', '+960'), ('+265', '+265'), ('+52', '+52'), ('+60', '+60'), ('+258', '+258'), ('+264', '+264'), ('+687', '+687'), ('+227', '+227'), ('+672', '+672'), ('+234', '+234'), ('+505', '+505'), ('+31', '+31'), ('+47', '+47'), ('+977', '+977'), ('+674', '+674'), ('+683', '+683'), ('+64', '+64'), ('+968', '+968'), ('+507', '+507'), ('+51', '+51'), ('+689', '+689'), ('+675', '+675'), ('+63', '+63'), ('+92', '+92'), ('+48', '+48'), ('+508', '+508'), ('+870', '+870'), ('+1', '+1'), ('+970', '+970'), ('+351', '+351'), ('+680', '+680'), ('+595', '+595'), ('+974', '+974'), ('+262', '+262'), ('+40', '+40'), ('+381', '+381'), ('+7', '+7'), ('+250', '+250'), ('+966', '+966'), ('+677', '+677'), ('+248', '+248'), ('+249', '+249'), ('+46', '+46'), ('+65', '+65'), ('+290', '+290'), ('+386', '+386'), ('+47', '+47'), ('+421', '+421'), ('+232', '+232'), ('+378', '+378'), ('+221', '+221'), ('+252', '+252'), ('+597', '+597'), ('+211', '+211'), ('+239', '+239'), ('+503', '+503'), ('+1-721', '+1-721'), ('+963', '+963'), ('+268', '+268'), ('+1-649', '+1-649'), ('+235', '+235'), ('+262', '+262'), ('+228', '+228'), ('+66', '+66'), ('+992', '+992'), ('+690', '+690'), ('+670', '+670'), ('+993', '+993'), ('+216', '+216'), ('+676', '+676'), ('+90', '+90'), ('+1-868', '+1-868'), ('+688', '+688'), ('+886', '+886'), ('+255', '+255'), ('+380', '+380'), ('+256', '+256'), ('+1', '+1'), ('+598', '+598'), ('+998', '+998'), ('+379', '+379'), ('+1-784', '+1-784'), ('+58', '+58'), ('+1-284', '+1-284'), ('+1-340', '+1-340'), ('+84', '+84'), ('+678', '+678'), ('+681', '+681'), ('+685', '+685'), ('+383', '+383'), ('+967', '+967'), ('+262', '+262'), ('+27', '+27'), ('+260', '+260'), ('+263', '+263')], max_length=4, null=True),
        ),
    ]
