import gettext

gettext.bindtextdomain('saccrec', './locales')
gettext.textdomain('saccrec')

_ = gettext.gettext
