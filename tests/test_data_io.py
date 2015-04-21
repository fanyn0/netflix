def first_n_indices_are_correct(point_generator, number_of_points, index):
    from itertools import islice
    from utils.data_io import data_points, indices
    from utils.data_paths import ALL_DATA_FILE_PATH, ALL_INDEX_FILE_PATH
    all_data = data_points(ALL_DATA_FILE_PATH)
    all_indices = indices(ALL_INDEX_FILE_PATH)
    point_generator_first_n = islice(point_generator, 0, number_of_points)
    for data_point in point_generator_first_n:
        for some_point in all_data:
            this_index = next(all_indices)
            if this_index == index:
                assert data_point == some_point
                break


def test_all_points_returns_a_generator():
    from types import GeneratorType
    from utils.data_io import all_points

    assert isinstance(all_points(), GeneratorType)


def test_all_points_first_ten_are_correct():
    from itertools import islice
    from utils.data_io import data_points
    from utils.data_io import all_points
    from utils.data_paths import ALL_DATA_FILE_PATH
    expected_all_points = data_points(ALL_DATA_FILE_PATH)
    actual_all_points_first_n = islice(all_points(), 0, 10)
    for actual_data_point in actual_all_points_first_n:
        expected_data_point = next(expected_all_points)
        assert actual_data_point == expected_data_point


def test_base_points_returns_a_generator():
    from types import GeneratorType
    from utils.data_io import base_points

    assert isinstance(base_points(), GeneratorType)


def test_base_points_first_ten_are_correct():
    from utils.constants import BASE_INDEX
    from utils.data_io import base_points
    first_n_indices_are_correct(base_points(), number_of_points=10,
                                index=BASE_INDEX)


def test_data_points_returns_a_generator():
    from types import GeneratorType
    from utils.data_io import data_points
    from utils.data_paths import ALL_DATA_FILE_PATH

    assert isinstance(data_points(ALL_DATA_FILE_PATH), GeneratorType)


def test_data_points_first_ten_are_correct():
    from utils.data_io import data_points
    from utils.data_paths import ALL_DATA_FILE_PATH

    data_points_generator = data_points(ALL_DATA_FILE_PATH)

    with open(ALL_DATA_FILE_PATH) as all_data_file:
        for _ in range(10):
            point_from_file = next(all_data_file).strip().split()
            point_from_generator = next(data_points_generator)
            assert point_from_generator == point_from_file


def test_get_user_movie_time_rating_returns_correct_values():
    from random import random
    from utils.constants import (MOVIE_INDEX, RATING_INDEX, TIME_INDEX,
                                 USER_INDEX)
    from utils.data_io import get_user_movie_time_rating
    unique_user = random()
    unique_movie = random()
    unique_time = random()
    unique_rating = random()
    data_point = [0] * 4
    data_point[USER_INDEX] = unique_user
    data_point[MOVIE_INDEX] = unique_movie
    data_point[TIME_INDEX] = unique_time
    data_point[RATING_INDEX] = unique_rating
    user, movie, time, rating = get_user_movie_time_rating(data_point)
    assert user == unique_user
    assert movie == unique_movie
    assert time == unique_time
    assert rating == unique_rating


def test_hidden_points_first_ten_are_correct():
    from utils.constants import HIDDEN_INDEX
    from utils.data_io import hidden_points
    first_n_indices_are_correct(hidden_points(), number_of_points=10,
                                index=HIDDEN_INDEX)


def test_hidden_points_returns_a_generator():
    from types import GeneratorType
    from utils.data_io import hidden_points

    assert isinstance(hidden_points(), GeneratorType)


def test_indices_first_ten_correct():
    from utils.data_io import indices
    from utils.data_paths import ALL_INDEX_FILE_PATH

    indices_generator = indices(ALL_INDEX_FILE_PATH)

    with open(ALL_INDEX_FILE_PATH) as all_index_file:
        for _ in range(10):
            assert next(indices_generator) == int(next(all_index_file).strip())


def test_load_data_returns_numpy_array():
    import numpy as np
    import os
    from utils.data_io import load_numpy_array_from_file
    from utils.data_paths import DATA_DIR_PATH
    expected_array = np.array([1, 2, 3, 4])
    array_file_name = 'test.npy'
    array_file_path = os.path.join(DATA_DIR_PATH, array_file_name)
    np.save(array_file_path, expected_array)
    try:
        actual_array = load_numpy_array_from_file(array_file_path)
        assert isinstance(actual_array, np.ndarray)
    finally:
        try:
            os.remove(array_file_path)
        except FileNotFoundError:
            pass


def test_load_numpy_array_from_file_returns_correct_array():
    import numpy as np
    import os
    from utils.data_io import load_numpy_array_from_file
    from utils.data_paths import DATA_DIR_PATH
    expected_array = np.array([1, 2, 3, 4])
    array_file_name = 'test.npy'
    array_file_path = os.path.join(DATA_DIR_PATH, array_file_name)
    np.save(array_file_path, expected_array)
    try:
        actual_array = load_numpy_array_from_file(array_file_path)
        np.testing.assert_array_equal(expected_array, actual_array)
    finally:
        try:
            os.remove(array_file_path)
        except FileNotFoundError:
            pass


def test_probe_points_first_ten_are_correct():
    from utils.constants import PROBE_INDEX
    from utils.data_io import probe_points
    first_n_indices_are_correct(probe_points(), number_of_points=10,
                                index=PROBE_INDEX)


def test_probe_points_returns_a_generator():
    from types import GeneratorType
    from utils.data_io import probe_points

    assert isinstance(probe_points(), GeneratorType)


def test_qual_points_first_ten_are_correct():
    from utils.constants import QUAL_INDEX
    from utils.data_io import qual_points
    first_n_indices_are_correct(qual_points(), number_of_points=10,
                                index=QUAL_INDEX)


def test_qual_points_returns_a_generator():
    from types import GeneratorType
    from utils.data_io import qual_points

    assert isinstance(qual_points(), GeneratorType)


def test_valid_points_first_ten_are_correct():
    from utils.constants import VALID_INDEX
    from utils.data_io import valid_points
    first_n_indices_are_correct(valid_points(), number_of_points=10,
                                index=VALID_INDEX)


def test_valid_points_returns_a_generator():
    from types import GeneratorType
    from utils.data_io import valid_points

    assert isinstance(valid_points(), GeneratorType)


def test_write_submission_creates_file():
    import os
    from utils.data_io import write_submission
    from utils.data_paths import SUBMISSIONS_DIR_PATH
    ratings = (1, 4, 3, 2, 5)
    submission_file_name = 'test.dta'
    submission_file_path = os.path.join(SUBMISSIONS_DIR_PATH,
                                        submission_file_name)
    assertion_message = '%s is for test use only' % submission_file_path
    assert not os.path.isfile(submission_file_path), assertion_message

    try:
        write_submission(ratings, submission_file_name)
        assertion_message = ('write_submission did not create %s' %
                             submission_file_path)
        assert os.path.isfile(submission_file_path), assertion_message
    finally:
        try:
            os.remove(submission_file_path)
        except FileNotFoundError:
            pass


def test_write_submission_writes_correct_ratings():
    import os
    from utils.data_io import write_submission
    from utils.data_paths import SUBMISSIONS_DIR_PATH
    ratings = (1, 4.0, 3.1, 2.01, 5.001)
    submission_file_name = 'test.dta'
    submission_file_path = os.path.join(SUBMISSIONS_DIR_PATH,
                                        submission_file_name)
    assertion_message = '%s is for test use only' % submission_file_path
    assert not os.path.isfile(submission_file_path), assertion_message

    try:
        write_submission(ratings, submission_file_name)
        with open(submission_file_path, 'r') as submission_file:
            for rating in ratings:
                assert float(next(submission_file).strip()) == float(rating)
    finally:
        try:
            os.remove(submission_file_path)
        except FileNotFoundError:
            pass