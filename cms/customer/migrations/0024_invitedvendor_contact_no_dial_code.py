# Generated by Django 2.2.5 on 2020-10-29 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0023_auto_20200908_1003'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitedvendor',
            name='contact_no_dial_code',
            field=models.CharField(blank=True, choices=[('880', '880'), ('32', '32'), ('226', '226'), ('359', '359'), ('387', '387'), ('+1-246', '+1-246'), ('681', '681'), ('590', '590'), ('+1-441', '+1-441'), ('673', '673'), ('591', '591'), ('973', '973'), ('257', '257'), ('229', '229'), ('975', '975'), ('+1-876', '+1-876'), ('', ''), ('267', '267'), ('685', '685'), ('599', '599'), ('55', '55'), ('+1-242', '+1-242'), ('+44-1534', '+44-1534'), ('375', '375'), ('501', '501'), ('7', '7'), ('250', '250'), ('381', '381'), ('670', '670'), ('262', '262'), ('993', '993'), ('992', '992'), ('40', '40'), ('690', '690'), ('245', '245'), ('+1-671', '+1-671'), ('502', '502'), ('', ''), ('30', '30'), ('240', '240'), ('590', '590'), ('81', '81'), ('592', '592'), ('+44-1481', '+44-1481'), ('594', '594'), ('995', '995'), ('+1-473', '+1-473'), ('44', '44'), ('241', '241'), ('503', '503'), ('224', '224'), ('220', '220'), ('299', '299'), ('350', '350'), ('233', '233'), ('968', '968'), ('216', '216'), ('962', '962'), ('385', '385'), ('509', '509'), ('36', '36'), ('852', '852'), ('504', '504'), (' ', ' '), ('58', '58'), ('+1-787 and 1-939', '+1-787 and 1-939'), ('970', '970'), ('680', '680'), ('351', '351'), ('47', '47'), ('595', '595'), ('964', '964'), ('507', '507'), ('689', '689'), ('675', '675'), ('51', '51'), ('92', '92'), ('63', '63'), ('870', '870'), ('48', '48'), ('508', '508'), ('260', '260'), ('212', '212'), ('372', '372'), ('20', '20'), ('27', '27'), ('593', '593'), ('39', '39'), ('84', '84'), ('677', '677'), ('251', '251'), ('252', '252'), ('263', '263'), ('966', '966'), ('34', '34'), ('291', '291'), ('382', '382'), ('373', '373'), ('261', '261'), ('590', '590'), ('212', '212'), ('377', '377'), ('998', '998'), ('95', '95'), ('223', '223'), ('853', '853'), ('976', '976'), ('692', '692'), ('389', '389'), ('230', '230'), ('356', '356'), ('265', '265'), ('960', '960'), ('596', '596'), ('+1-670', '+1-670'), ('+1-664', '+1-664'), ('222', '222'), ('+44-1624', '+44-1624'), ('256', '256'), ('255', '255'), ('60', '60'), ('52', '52'), ('972', '972'), ('33', '33'), ('246', '246'), ('290', '290'), ('358', '358'), ('679', '679'), ('500', '500'), ('691', '691'), ('298', '298'), ('505', '505'), ('31', '31'), ('47', '47'), ('264', '264'), ('678', '678'), ('687', '687'), ('227', '227'), ('672', '672'), ('234', '234'), ('64', '64'), ('977', '977'), ('674', '674'), ('683', '683'), ('682', '682'), ('', ''), ('225', '225'), ('41', '41'), ('57', '57'), ('86', '86'), ('237', '237'), ('56', '56'), ('61', '61'), ('1', '1'), ('242', '242'), ('236', '236'), ('243', '243'), ('420', '420'), ('357', '357'), ('61', '61'), ('506', '506'), ('599', '599'), ('238', '238'), ('53', '53'), ('268', '268'), ('963', '963'), ('599', '599'), ('996', '996'), ('254', '254'), ('211', '211'), ('597', '597'), ('686', '686'), ('855', '855'), ('+1-869', '+1-869'), ('269', '269'), ('239', '239'), ('421', '421'), ('82', '82'), ('386', '386'), ('850', '850'), ('965', '965'), ('221', '221'), ('378', '378'), ('232', '232'), ('248', '248'), ('7', '7'), ('+1-345', '+1-345'), ('65', '65'), ('46', '46'), ('249', '249'), ('+1-809 and 1-829', '+1-809 and 1-829'), ('+1-767', '+1-767'), ('253', '253'), ('45', '45'), ('+1-284', '+1-284'), ('49', '49'), ('967', '967'), ('213', '213'), ('1', '1'), ('598', '598'), ('262', '262'), ('1', '1'), ('961', '961'), ('+1-758', '+1-758'), ('856', '856'), ('688', '688'), ('886', '886'), ('+1-868', '+1-868'), ('90', '90'), ('94', '94'), ('423', '423'), ('371', '371'), ('676', '676'), ('370', '370'), ('352', '352'), ('231', '231'), ('266', '266'), ('66', '66'), ('', ''), ('228', '228'), ('235', '235'), ('+1-649', '+1-649'), ('218', '218'), ('379', '379'), ('+1-784', '+1-784'), ('971', '971'), ('376', '376'), ('+1-268', '+1-268'), ('93', '93'), ('+1-264', '+1-264'), ('+1-340', '+1-340'), ('354', '354'), ('98', '98'), ('374', '374'), ('355', '355'), ('244', '244'), ('', ''), ('+1-684', '+1-684'), ('54', '54'), ('61', '61'), ('43', '43'), ('297', '297'), ('+91', '+91'), ('+358-18', '+358-18'), ('994', '994'), ('353', '353'), ('62', '62'), ('380', '380'), ('974', '974'), ('258', '258')], max_length=4, null=True),
        ),
    ]
