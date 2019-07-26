import tensorflow as tf

x = tf.placeholder(tf.int32, name="x")
w = tf.Variable(1, dtype=tf.int32, name='w')
b = tf.Variable("You are: ")
c = tf.constant(2, dtype=tf.int32, name='odd')


def flag():
    flag_string = tf.read_file('/flag', name='getflag')
    return flag_string


def even():
    def fail():
        return tf.constant('Bot')

    ans = tf.cond(tf.equal(x, 1024), flag, fail, name='flag')

    return ans


def odd():
    return tf.constant('Human')


first = tf.mod(x, c)
ans = tf.cond(tf.equal(first, 0), even, odd, name="Answer")
y = tf.string_join([b, ans], name='y')
saver = tf.train.Saver()
sess = tf.Session()
sess.run(tf.global_variables_initializer())
# y_out = sess.run(y, {'x:0': 1028})

# print(y_out)
saver.save(sess, 'detection_model/detection')
