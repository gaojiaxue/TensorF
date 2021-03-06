import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

# add one layer


def add_layer(inputs, in_size, out_size,n_layer, activation_function=None):
    # name each part
    layer_name='layer%s'%(n_layer)
    with tf.name_scope(layer_name):
        with tf.name_scope('weights'):
            Weights = tf.Variable(tf.random_normal([in_size, out_size]))
            #show tensor in tensorboard
            tf.summary.histogram(layer_name+'/weights',Weights)
        with tf.name_scope('biases'):
            biases = tf.Variable(tf.zeros([1, out_size])+0.1)
            tf.summary.histogram(layer_name+'/biases',biases)
        with tf.name_scope('Wx_plus_b'):
            Wx_plus_b = tf.matmul(inputs, Weights)+biases
            if activation_function is None:
                outputs = Wx_plus_b
            else:
                outputs = activation_function(Wx_plus_b)
            tf.summary.histogram(layer_name+'/outputs',outputs)
            return outputs


# assume data
# [:,np.newaxis]make matrix shape changed
x_data = np.linspace(-1, 1, 300)[:, np.newaxis]
noise = np.random.normal(0, 0.05, x_data.shape)
y_data = np.square(x_data)-0.5+noise
with tf.name_scope('Inputs'):
    xs = tf.placeholder(tf.float32, [None, 1], name='x_input')
    ys = tf.placeholder(tf.float32, [None, 1], name='y_input')
# first layer
l1 = add_layer(xs,1,10,1,activation_function=tf.nn.relu)
#second layer
prediction = add_layer(l1,10,2,1,activation_function=None)
# reduction_indices[0]means push row in to one ,[1]means push column into one, [0,1]or [1,0]means push to a point
with tf.name_scope('loss'):
    loss = tf.reduce_mean(tf.reduce_sum(
        tf.square(ys-prediction), reduction_indices=[1]))
    #show Scalar in tensorboard
    tf.summary.scalar('loss',loss)
with tf.name_scope('train'):
    train_step = tf.train.GradientDescentOptimizer(0.1).minimize(loss)
init = tf.initialize_all_variables()

sess = tf.Session()
merged=tf.summary.merge_all()
# write all parts into a picture
writer = tf.summary.FileWriter("logs/",sess.graph)
sess.run(init)
# show the orginal data
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.scatter(x_data, y_data)
# keep show use ion()
plt.ion()
plt.show()
for i in range(1000):
     sess.run(train_step, feed_dict={xs: x_data, ys: y_data})
     if i % 50 == 0:
         result=sess.run(merged,feed_dict={xs:x_data,ys:y_data})
         writer.add_summary(result,i)
# for i in range(1000):
#     sess.run(train_step, feed_dict={xs: x_data, ys: y_data})
#     if i % 50 == 0:
#         try:
#             ax.lines.remove(lines[0])
#         except Exception:
#             pass
#         prediction_value = sess.run(prediction, feed_dict={
#                                     xs: x_data, ys: y_data})
#         lines = ax.plot(x_data, prediction_value, 'r-', lw=5)
#         plt.pause(0.1)
    #   print(sess.run(loss,feed_dict={xs:x_data,ys:y_data}))

