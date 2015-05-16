import numpy as np
import pickle
from utils.constants import USER_INDEX, MOVIE_INDEX, RATING_INDEX, BLENDING_RATIO


class DataStats():
    def __init__(self):
        self.data_set = []
        self.num_users = None
        self.num_movies = None
        self.global_average = None
        self.movie_averages = []
        self.movie_rating_count = []
        self.movie_rating_sum = []
        self.user_offsets = []
        self.user_rating_count = []
        self.user_offsets_sum = []

    def init_movie_and_user_arrays(self):
        self.movie_averages = np.zeros(shape=(self.num_movies,), dtype=np.float32)
        self.movie_rating_count = np.zeros(shape=(self.num_movies,), dtype=np.int32)
        self.movie_rating_sum = np.zeros(shape=(self.num_movies,))
        self.user_offsets_sum = np.zeros(shape=(self.num_users,))
        self.user_offsets = np.zeros(shape=(self.num_users,), dtype=np.float32)
        self.user_rating_count = np.zeros(shape=(self.num_users,), dtype=np.int32)

    def load_data_set(self, data_set):
        self.data_set = data_set
        self.num_users = np.amax(data_set[:, USER_INDEX]) + 1
        self.num_movies = np.amax(data_set[:, MOVIE_INDEX]) + 1

    def compute_stats(self):
        if self.data_set == []:
            raise Exception('No Data set loaded. Please use DataStats.load_data_set' +
                            '(data_set) to load a data set before calling compute_stats')
        else:
            self.init_movie_and_user_arrays()
            self.compute_movie_stats()
            self.compute_user_stats()

    def compute_movie_stats(self):
        simple_sum, simple_count = compute_simple_indexed_sum_and_count(
            data_values=self.data_set[:, RATING_INDEX],
            data_indices=self.data_set[:, MOVIE_INDEX]
            )
        global_average = compute_global_average_rating(data_set=self.data_set)
        self.movie_averages = compute_blended_indexed_averages(
            simple_sum=simple_sum,
            simple_count=simple_count,
            global_average=global_average
            )
        self.movie_rating_count = simple_count
        self.movie_rating_sum = simple_sum
        self.global_average = global_average

    def compute_user_stats(self):
        simple_offsets = compute_offsets(
            data_indices=self.data_set[:, MOVIE_INDEX],
            data_values=self.data_set[:, RATING_INDEX],
            averages=self.movie_averages)
        simple_sum, simple_count = compute_simple_indexed_sum_and_count(
            data_indices=self.data_set[:, USER_INDEX],
            data_values=simple_offsets,
        )
        user_offset_global_average = np.sum(simple_sum)/np.sum(simple_count)
        if user_offset_global_average == np.nan:
            raise Exception('Error NaN in global average of offsets')
        self.user_offsets = compute_blended_indexed_averages(
            simple_sum=simple_sum,
            simple_count=simple_count,
            global_average=user_offset_global_average
        )
        self.user_offsets_sum = simple_sum
        self.user_rating_count = simple_count

    def get_baseline(self, user, movie):
        if self.movie_averages == []:
            raise Exception('Cannot get baseline: Missing Movie averages!')
        if self.user_offsets == []:
            raise Exception('Cannot get baseline: Missing user offsets!')
        mov_avg = self.movie_averages[movie]
        usr_off = self.user_offsets[user]
        return mov_avg + usr_off

    def write_stats_to_file(self, file_path):
        self.data_set = []
        pickle.dump(self, file=open(file_path, 'wb'))


def compute_simple_indexed_sum_and_count(data_indices, data_values):
    if data_indices.shape != data_values.shape:
        raise ValueError('Error! Shapes of index array and data array are not the same!')
    array_length = np.amax(data_indices) + 1
    data = zip(data_indices, data_values)
    indexed_sum = np.zeros(shape=(array_length,), dtype=np.float32)
    indexed_count = np.zeros(shape=(array_length,), dtype=np.int32)
    for index, value in data:
        indexed_sum[index] += value
        indexed_count[index] += 1
    return indexed_sum, indexed_count


def compute_offsets(data_values, data_indices, averages):
    offsets = np.zeros(shape=data_values.shape, dtype=np.float32)
    for index, value in enumerate(data_values):
        offsets[index] += value - averages[data_indices[index]]
    return offsets


def compute_blended_indexed_averages(simple_sum, simple_count, global_average):
    return np.array([((global_average * BLENDING_RATIO + simple_sum[i])/(BLENDING_RATIO + simple_count[i]))
                     for i in range(len(simple_sum))])


def compute_global_average_rating(data_set):
    from utils.constants import RATING_INDEX
    return np.mean(data_set[:, RATING_INDEX])


def load_stats_from_file(file_path):
    pickle_file = open(file_path, 'rb')
    stats_object = pickle.load(pickle_file)
    return stats_object

