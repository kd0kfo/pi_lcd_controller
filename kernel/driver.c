/**
 *
 * This is a driver for buttons on the Raspberry Pi. It will accept via write a byte that is
 * a bitmask for buttons being pressed (1) or not (0). When read, the driver will
 * return a byte per button, equal to 1 if the button is down or 0 if it is not.
 *
 * If fewer than the number of buttons is attempted to be read, the output will be truncated
 * to the number of buttons available. If more than one byte is written to the driver,
 * only the last byte is used, because it is assumed that is the newest state.
 * 
 * For user access add the following to a /etc/udev/rules.d/99-buttons.rules file:
 * KERNEL=="buttons", SUBSYSTEM=="buttons_class", MODE="0666"
 *
 */
#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/device.h>
#include <linux/fs.h>
#include <linux/mutex.h>
#include <asm/uaccess.h>

#define DEVICE_NAME "buttons"
#define CLASS_NAME "buttons_class"
#define BUFFER_SIZE 8

MODULE_LICENSE("GPL");
MODULE_AUTHOR("David Coss");
MODULE_DESCRIPTION("Raspberry Pi Button Driver");
MODULE_VERSION("0.1");

static char the_buffer[BUFFER_SIZE];
static int major_number;
static struct class *bd_class = NULL;
static struct device *bd_device = NULL;
static char *bd_name = DEVICE_NAME;
module_param(bd_name, charp, S_IRUGO);
static DEFINE_MUTEX(bd_mutex);



static int bd_open(struct inode *the_inode, struct file *the_file) {
	printk(KERN_INFO "Opened button driver file\n");
	return 0;
}

static ssize_t bd_read(struct file *fp, char *buffer, size_t len, loff_t *offset) {
	ssize_t readlen = (len > BUFFER_SIZE) ? BUFFER_SIZE : len;
	memcpy(buffer, the_buffer, readlen);

	printk(KERN_INFO "Read %lu bytes\n", readlen);
	return readlen;
}


static ssize_t bd_write(struct file *fp, const char *buffer, size_t len, loff_t *offset) {
	unsigned char curr_state = 0;
	size_t amountwritten = len;
	int i = 0;
	if (len == 0)
		return 0;

	if (!mutex_trylock(&bd_mutex)) {
		printk(KERN_INFO "File busy\n");
		return -EBUSY;
	}
	curr_state = (unsigned char)buffer[len - 1]; // Only use last.
	i = 0;
	for (;i<BUFFER_SIZE;i++) {
		the_buffer[i] = curr_state & 1;
		curr_state >>= 1;
	}

	mutex_unlock(&bd_mutex);
	return amountwritten;
}

static int the_bd_release(struct inode *the_inode, struct file *fp) {
	printk(KERN_INFO "Button device file closed\n");
	return 0;
}

static struct file_operations fops = {
	.open = bd_open,
	.read = bd_read,
	.write = bd_write,
	.release = the_bd_release,
};

static int __init bd_init(void) {
	mutex_init(&bd_mutex);
	major_number = register_chrdev(0, DEVICE_NAME, &fops);
	if (major_number < 0) {
		printk(KERN_ALERT "Button driver failed to register a major number\n");
		mutex_destroy(&bd_mutex);
		return major_number;
	}
	
	bd_class = class_create(THIS_MODULE, CLASS_NAME);
	if (IS_ERR(bd_class)) {
		unregister_chrdev(major_number, DEVICE_NAME);
		printk(KERN_ALERT "Failed to register device class\n");
		mutex_destroy(&bd_mutex);
		return PTR_ERR(bd_class);
	}

	bd_device = device_create(bd_class, NULL, MKDEV(major_number,0 ), NULL, DEVICE_NAME);
	if (IS_ERR(bd_device)) {
		class_destroy(bd_class);
		unregister_chrdev(major_number, DEVICE_NAME);
		printk(KERN_ALERT "Failed to create device\n");
		mutex_destroy(&bd_mutex);
		return PTR_ERR(bd_device);
	}

	memset(the_buffer, 0, BUFFER_SIZE * sizeof(char));
	printk(KERN_INFO "Starting button driver\n");
	return 0;
}

static void __exit bd_exit(void) {
	device_destroy(bd_class, MKDEV(major_number, 0));
	class_unregister(bd_class);
	class_destroy(bd_class);
	unregister_chrdev(major_number, DEVICE_NAME);
	mutex_destroy(&bd_mutex);
	printk(KERN_INFO "Unloaded button driver\n");
}

module_init(bd_init);
module_exit(bd_exit);
