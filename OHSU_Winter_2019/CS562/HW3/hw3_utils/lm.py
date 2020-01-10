import torch
import torch.nn as nn
import random
import numpy as np
import matplotlib.pyplot as plt
import itertools
from hw3_utils import vocab

class NameGenerator(nn.Module):
    def __init__(self, input_vocab_size, n_embedding_dims, n_hidden_dims, n_lstm_layers, output_vocab_size):
        """
        Initialize our name generator, following the equations laid out in the assignment. In other words,
        we'll need an Embedding layer, an LSTM layer, a Linear layer, and LogSoftmax layer.

        Note: Remember to set batch_first=True when initializing your LSTM layer!

        Also note: When you build your LogSoftmax layer, pay attention to the dimension that you're
        telling it to run over!
        """
        super(NameGenerator, self).__init__()
        #self.lstm_dims = n_hidden_dims
        #self.lstm_layers = n_lstm_layers
        #raise NotImplementedError

        self.lstm_dims = n_hidden_dims
        self.lstm_layers = n_lstm_layers

        self.input_lookup = nn.Embedding(num_embeddings=input_vocab_size,
                                          embedding_dim=n_embedding_dims)

        self.lstm = nn.LSTM(input_size=n_embedding_dims,
                            hidden_size=n_hidden_dims,
                            num_layers=n_lstm_layers,
                            batch_first=True)

        self.output = nn.Linear(in_features=n_hidden_dims,
                                out_features=output_vocab_size)

        self.softmax = nn.LogSoftmax(dim=2)

    def forward(self, history_tensor, prev_hidden_state):
        """
        Given a history, and a previous timepoint's hidden state, predict the next character.

        Note: Make sure to return the LSTM hidden state, so that we can use this for
        sampling/generation in a one-character-at-a-time pattern, as in Goldberg 9.5!
        """

        embeds = self.input_lookup(history_tensor)

        lstm_out, hn_cn = self.lstm(embeds, prev_hidden_state)

        lin_out = self.output(lstm_out)

        sftm_out = self.softmax(lin_out)

        return  (sftm_out, hn_cn)

    def init_hidden(self):
        """
        Generate a blank initial history value, for use when we start predicting over a fresh sequence.
        """
        h_0 = torch.randn(self.lstm_layers, 1, self.lstm_dims)
        c_0 = torch.randn(self.lstm_layers, 1, self.lstm_dims)

        return (h_0, c_0)
### Utility functions

def train(model, epochs, training_data, c2i):
    """
    Train model for the specified number of epochs, over the provided training data.

    Make sure to shuffle the training data at the beginning of each epoch!
    """

    opt = torch.optim.Adam(model.parameters())

    loss_function = torch.nn.NLLLoss()

    loss_batch_size = 100

    for _ in range(epochs):

        random.shuffle(training_data)

        loss = 0

        for idx, name in enumerate(training_data):

            if idx % loss_batch_size == 0:
                opt.zero_grad()

            x_tens = vocab.sentence_to_tensor(name[:-1], c2i, True)
            y_tens = vocab.sentence_to_tensor(name[1:], c2i, True)

            y_hat, _ = model(x_tens, model.init_hidden())


            loss += loss_function(y_hat[-1],y_tens[-1])

            if idx % 1000 == 0:
                print(f"{idx}/{len(training_data)} average per-item loss: {loss / loss_batch_size}")

            if idx % loss_batch_size == 0 and idx > 0:
                # send back gradients:
                loss.backward()
                # now, tell the optimizer to update our weights:
                opt.step()
                loss = 0

        # now one last time:
        loss.backward()
        opt.step()

    return model



def sample(model, c2i, i2c, max_seq_len=200):
    """
    Sample a new sequence from model.

    The length of the resulting sequence should be < max_seq_len, and the 
    new sequence should be stripped of <bos>/<eos> symbols if necessary.
    """
    with torch.no_grad():
        the_string = ''
        #string_builder = torch.tensor([[c2i[vocab.BOS_SYM]]])
        string_builder = torch.tensor([[c2i['L']]])
        y_hat, state = model(string_builder, model.init_hidden())

        row_of_vals = y_hat[0,-1]

        #val, indx = row_of_vals.max(0)

        total_prob = int(row_of_vals.sum())
        list_of_ind = []
        threshold = -6
        for i in range(len(row_of_vals)):
            print(float(row_of_vals[i]))
            if float(row_of_vals[i]) > threshold:
                list_of_ind.append(i)

        indx = random.choice(list_of_ind)


        new_char = i2c[int(indx)]
        the_string += new_char


        print(string_builder)
        print(val)
        string_builder = torch.cat((string_builder,torch.tensor([[int(indx)]])), dim=1)
        print(string_builder)

        for _ in range(max_seq_len):
            if new_char == vocab.EOS_SYM:
                return the_string[:-1]

            y_hat, state = model(string_builder, state)

            row_of_vals = y_hat[0,-1]
            val, indx = row_of_vals.max(0)
            new_char = i2c[int(indx)]
            the_string += new_char

        return the_string





def compute_prob(model, sentence, c2i):
    """
    Compute the negative log probability of p(sentence)

    Equivalent to equation 3.3 in Jurafsky & Martin.
    """

    nll = nn.NLLLoss(reduction='sum')

    with torch.no_grad():
        s_tens = vocab.sentence_to_tensor(sentence, c2i, True)
        x = s_tens[:,:-1]
        y = s_tens[:,1:]
        y_hat, _ = model(x, model.init_hidden())
        return nll(y_hat.squeeze(), y.squeeze()).item() # get rid of first dimension of each







