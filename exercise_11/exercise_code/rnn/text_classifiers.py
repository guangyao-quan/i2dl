import torch
import torch.nn as nn
from torch.nn.utils.rnn import pack_padded_sequence
from .rnn_nn import Embedding, RNN, LSTM

class RNNClassifier(nn.Module):
    def __init__(self, num_embeddings, embedding_dim, hidden_size, use_lstm=True, **additional_kwargs):
        """
        Inputs:
            num_embeddings: size of the vocabulary
            embedding_dim: size of an embedding vector
            hidden_size: hidden_size of the rnn layer
            use_lstm: use LSTM if True, vanilla RNN if false, default=True
        """
        super().__init__()
        # Change this if you edit arguments
        hparams = {
            'num_embeddings': num_embeddings,
            'embedding_dim': embedding_dim,
            'hidden_size': hidden_size,
            'use_lstm': use_lstm,
            **additional_kwargs
        }
        # if you do not inherit from lightning module use the following line
        self.hparams = hparams
        # if you inherit from lightning module, comment out the previous line and use the following line
        # self.hparams.update(hparams)
        
        ########################################################################
        # TODO: Initialize an RNN network for sentiment classification         #
        # hint: A basic architecture can have an embedding, an rnn             #
        # and an output layer                                                  #
        ########################################################################
        """self.embedding = Embedding(self.hparams['num_embeddings'], self.hparams['embedding_dim'], 0)
        self.lstm = nn.LSTM(self.hparams['embedding_dim'], self.hparams['hidden_size'])
        self.fc = nn.Linear(in_features=self.hparams['hidden_size'], out_features=1)
        self.sig = nn.Sigmoid()"""
        # created by Copilot
        self.encoder = nn.Embedding(self.hparams['num_embeddings'], self.hparams['embedding_dim'])
        self.rnn = LSTM(self.hparams['embedding_dim'], self.hparams['hidden_size'])
        self.decoder = nn.Linear(self.hparams['hidden_size'], 1) # 1 for bianry classification
        # created by Copilot
        pass
        ########################################################################
        #                           END OF YOUR CODE                           #
        ########################################################################

    def forward(self, sequence, lengths=None):
        """
        Inputs
            sequence: A long tensor of size (seq_len, batch_size)
            lengths: A long tensor of size batch_size, represents the actual
                sequence length of each element in the batch. If None, sequence
                lengths are identical.
        Outputs:
            output: A 1-D tensor of size (batch_size,) represents the probabilities of being
                positive, i.e. in range (0, 1)
        """
        output = None
        ########################################################################
        # TODO: Apply the forward pass of your network                         #
        # hint: Don't forget to use pack_padded_sequence if lenghts is not None#
        # pack_padded_sequence should be applied to the embedding outputs      #
        ########################################################################
        """embeddings = self.embedding(sequence)
        if lengths is not None:
            embeddings = pack_padded_sequence(embeddings, lengths)
        _, (h_n, c_n) = self.lstm(embeddings)
        dense = self.fc(h_n)
        sig_out = self.sig(dense)
        output = sig_out[-1, :, :].squeeze(1)
        pass"""
        # created by Copilot
        embeddings = self.encoder(sequence)
        if lengths is not None:
            embeddings = pack_padded_sequence(embeddings, lengths)
        rnn_out, _ = self.rnn(embeddings)
        dense = self.decoder(rnn_out)
        output = dense[-1, :, :].squeeze(1)
        # created by Copilot
        ########################################################################
        #                           END OF YOUR CODE                           #
        ########################################################################
        return output

