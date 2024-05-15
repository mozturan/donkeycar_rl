
from keras.layers import Conv2D, MaxPooling2D,UpSampling2D
import keras
from keras.optimizers.legacy import Adam

class ConvolutionalAutoencoder:
    def __init__(self, input_shape=(120, 160, 3), num_filters=[32, 64, 128]):
        self.input_shape = input_shape
        self.num_filters = num_filters
        self.autoencoder = self.build_autoencoder()

    def build_autoencoder(self):
        input_img = keras.Input(shape=self.input_shape)
        x = input_img

        # Encoder
        for filters in self.num_filters:
            x = Conv2D(filters, (5,5), activation='relu', padding='same')(x)
            x = MaxPooling2D((2, 2), padding='same')(x)
        encoded = x

        # Decoder
        for filters in reversed(self.num_filters):
            x = Conv2D(filters, (5,5), activation='relu', padding='same')(x)
            x = UpSampling2D((2, 2))(x)
        decoded = Conv2D(3, (5,5), activation='sigmoid', padding='same')(x)

        autoencoder = keras.Model(input_img, decoded)
        autoencoder.compile(optimizer=Adam(0.001), loss='mse')
        return autoencoder    
    
    def train(self, X_train, X_test, epochs=50, batch_size=128):
        self.autoencoder.fit(X_train, X_train,
                             epochs=epochs,
                             batch_size=batch_size,
                             shuffle=True,
                             validation_data=(X_test, X_test))

    def predict(self, X):
        
        # Predicts reconstruction for given images
        
        return self.autoencoder.predict(X)

    
    def summary(self):
        """
        Prints a summary of the Autoencoder's architecture
        """
        print("Autoencoder Architecture:")
        self.autoencoder.summary()

    def save(self, encoder_file="encoder_model.json", weights_file="encoder_weights.h5"):
        encoder = keras.Model(inputs=self.autoencoder.input, outputs=self.autoencoder.get_layer(index=-7).output)
        encoder_json = encoder.to_json()
        with open(encoder_file, "w") as json_file:
            json_file.write(encoder_json)
        encoder.save_weights(weights_file)

    """
    from keras.models import model_from_json
    # Load the encoder model architecture from the JSON file
    with open('encoder_model.json', 'r') as json_file:
        loaded_model_json = json_file.read()
    loaded_encoder = model_from_json(loaded_model_json)

    # Load the encoder model weights from the HDF5 file
    loaded_encoder.load_weights("encoder_weights.h5")
    """