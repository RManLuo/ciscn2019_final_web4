import tensorflow as tf
from tensorflow.python import pywrap_tensorflow


def init(model_path):
    new_sess = tf.Session()
    meta_file = model_path + ".meta"
    model = model_path
    saver = tf.train.import_meta_graph(meta_file)
    saver.restore(new_sess, model)
    return new_sess


def renew(sess, model_path):
    sess.close()
    return init(model_path)


def predict(sess, x):
    '''

    :param x: input number x
        sess: tensorflow session
    :return: b'You are: *'
        odd： You are : human,
        even： You are : bot,
    '''
    y = sess.graph.get_tensor_by_name("y:0")
    y_out = sess.run(y, {"x:0": x})
    return y_out


if __name__ == '__main__':
    sess = init("detection_model/detection")
    for i in range(400):
        print(predict(sess, 0), predict(sess, 1))
    sess = renew(sess, "detection_model/detection")
    print(predict(sess, 0), predict(sess, 1))
