# rc-boot driver for lilo

LOADER_CONFIG=/etc/yaboot.conf

rc_boot_prep_image () {
	if [ "$GRUB_ONLY" != "" ] && is_yes "$GRUB_ONLY" ; then 
		return 0
	fi
}

rc_boot_init () {

OFBOOT=`ofpath $BOOT`

	cat <<!EOF!
# By default boot the $DEFAULT entry
boot=${BOOT}
ofboot=${OFBOOT}
default=${DEFAULT}
timeout=${TIMEOUT}0
delay=${TIMEOUT}0
install=/lib/yaboot/yaboot
magicboot=/lib/yaboot/ofboot
enablecdboot
enableofboot
!EOF!

}

rc_boot_image () {
	if [ "$GRUB_ONLY" != "" ] && is_yes "$GRUB_ONLY" ; then 
		return 0
	fi
  
	case "$TYPE" in
	linux)  # This is Linux. Lets make an entry 
		# for this in /etc/yaboot.conf
		echo "# Linux image"
		echo "image=${KERNEL}"
		echo "	root=${ROOT}"
		echo "	label=${NAME}"
		[ "${APPEND}" != "" ] 	&& echo "	append=\"${APPEND}\""
		[ "$INITRD" != "" ] 	&& echo "	initrd=${INITRD}"
		echo "read-only"
		;;
	macos)  # This is MacOS. Lets make an entry 
		# for this in /etc/yaboot.conf
		echo "# MacOS image"
		echo "macos=${ROOT}"
		;;
	*)	# Buuu 
		die "Don't know how to handle OS type = '$TYPE'"
		;;
	esac
}

rc_boot_fini () {
	echo "# EOF"
}


rc_boot_run () {
	ybin >/dev/null 2>&1
}

# Thats all folk.
