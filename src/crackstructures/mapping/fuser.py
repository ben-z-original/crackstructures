import torch
import numpy as np


class NaiveMaxFuser:
    def __init__(self, class_weight=None):
        self.class_weight = class_weight

    def __call__(self, probabilities, viewing_conditions):
        probabilities = probabilities * self.class_weight if self.class_weight is not None else probabilities

        # apply angle constraint on views
        probabilities[(270 < viewing_conditions.angles) + (viewing_conditions.angles < 90), :] = torch.nan
        probabilities = torch.nan_to_num(probabilities, nan=0)
        aggr = probabilities.max(dim=1).values

        # Note: aggr[:, 0] is assumed to be the default/background class
        aggr[:, 1:] = torch.nan_to_num(aggr[:, 1:], nan=0.0)
        aggr[:, 0] = torch.where(torch.isnan(aggr[:, 0]), 1 - aggr[:, 1:].sum(dim=1), aggr[:, 0])
        argmax = torch.argmax(aggr, dim=1)
        return aggr, argmax


class NaiveMeanFuser:
    def __init__(self, class_weight=None):
        self.class_weight = class_weight

    def __call__(self, probabilities, viewing_conditions):
        probabilities = probabilities * self.class_weight if self.class_weight is not None else probabilities

        # apply angle constraint on views
        probabilities[(270 < viewing_conditions.angles) + (viewing_conditions.angles < 90), :] = torch.nan
        aggr = torch.nanmean(probabilities, dim=1)

        # Note: aggr[:, 0] is assumed to be the default/background class
        aggr[:, 1:] = torch.nan_to_num(aggr[:, 1:], nan=0.0)
        aggr[:, 0] = torch.where(torch.isnan(aggr[:, 0]), 1 - aggr[:, 1:].sum(dim=1), aggr[:, 0])
        argmax = torch.argmax(aggr, dim=1)
        return aggr, argmax


class NaiveMedianFuser:
    def __init__(self, class_weight=None):
        self.class_weight = class_weight

    def __call__(self, probabilities, viewing_conditions):
        probabilities = probabilities * self.class_weight if self.class_weight is not None else probabilities

        # apply angle constraint on views
        probabilities[(270 < viewing_conditions.angles) + (viewing_conditions.angles < 90), :] = torch.nan
        aggr = torch.nanmedian(probabilities, dim=1).values

        # Note: aggr[:, 0] is assumed to be the default/background class
        aggr[:, 1:] = torch.nan_to_num(aggr[:, 1:], nan=0.0)
        aggr[:, 0] = torch.where(torch.isnan(aggr[:, 0]), 1 - aggr[:, 1:].sum(dim=1), aggr[:, 0])
        argmax = torch.argmax(aggr, dim=1)
        return aggr, argmax


class AngleBestFuser:
    def __init__(self, class_weight=None):
        self.class_weight = class_weight

    def __call__(self, probabilities, viewing_conditions):
        probabilities = probabilities * self.class_weight if self.class_weight is not None else probabilities

        # apply angle constraint on views
        angle_dev = np.abs(viewing_conditions.angles - 180)
        probabilities[(angle_dev != angle_dev.min(axis=1)[:, None]), :] = torch.nan
        aggr = torch.nanmean(probabilities, dim=1)

        # Note: aggr[:, 0] is assumed to be the default/background class
        aggr[:, 1:] = torch.nan_to_num(aggr[:, 1:], nan=0.0)
        aggr[:, 0] = torch.where(torch.isnan(aggr[:, 0]), 1 - aggr[:, 1:].sum(dim=1), aggr[:, 0])
        argmax = torch.argmax(aggr, dim=1)
        return aggr, argmax


class AngleRangeFuser:
    def __init__(self, class_weight=None):
        self.class_weight = class_weight

    def __call__(self, probabilities, viewing_conditions):
        probabilities = probabilities * self.class_weight if self.class_weight is not None else probabilities

        # apply angle constraint on views
        probabilities[(230 < viewing_conditions.angles) + (viewing_conditions.angles < 130), :] = torch.nan
        aggr = torch.nanmean(probabilities, dim=1)

        # Note: aggr[:, 0] is assumed to be the default/background class
        aggr[:, 1:] = torch.nan_to_num(aggr[:, 1:], nan=0.0)
        aggr[:, 0] = torch.where(torch.isnan(aggr[:, 0]), 1 - aggr[:, 1:].sum(dim=1), aggr[:, 0])
        argmax = torch.argmax(aggr, dim=1)
        return aggr, argmax


class AngleWeightedFuser:
    def __init__(self, class_weight=None):
        self.class_weight = class_weight

    def __call__(self, probabilities, viewing_conditions):
        probabilities = probabilities * self.class_weight if self.class_weight is not None else probabilities

        # apply angle constraint on views
        weight = np.maximum(0, -np.cos(np.deg2rad(viewing_conditions.angles)))
        probabilities *= weight[..., None]

        aggr = torch.nanmean(probabilities, dim=1)

        # Note: aggr[:, 0] is assumed to be the default/background class
        aggr[:, 1:] = torch.nan_to_num(aggr[:, 1:], nan=0.0)
        aggr[:, 0] = torch.where(torch.isnan(aggr[:, 0]), 1 - aggr[:, 1:].sum(dim=1), aggr[:, 0])
        argmax = torch.argmax(aggr, dim=1)
        return aggr, argmax


class DistanceBestFuser:
    def __init__(self, class_weight=None):
        self.class_weight = class_weight

    def __call__(self, probabilities, viewing_conditions):
        probabilities = probabilities * self.class_weight if self.class_weight is not None else probabilities

        # apply angle constraint on views
        probabilities[(270 < viewing_conditions.angles) + (viewing_conditions.angles < 90), :] = torch.nan
        # TODO: nan in distances
        probabilities[(viewing_conditions.distances != np.max(viewing_conditions.distances, axis=1)[:, None]),
        :] = torch.nan
        aggr = torch.nanmean(probabilities, dim=1)

        # Note: aggr[:, 0] is assumed to be the default/background class
        aggr[:, 1:] = torch.nan_to_num(aggr[:, 1:], nan=0.0)
        aggr[:, 0] = torch.where(torch.isnan(aggr[:, 0]), 1 - aggr[:, 1:].sum(dim=1), aggr[:, 0])
        argmax = torch.argmax(aggr, dim=1)
        return aggr, argmax


class DistanceRangeFuser:
    def __init__(self, class_weight=None):
        self.class_weight = class_weight

    def __call__(self, probabilities, viewing_conditions):
        probabilities = probabilities * self.class_weight if self.class_weight is not None else probabilities

        # apply angle constraint on views
        probabilities[(270 < viewing_conditions.angles) + (viewing_conditions.angles < 90), :] = torch.nan
        probabilities[(viewing_conditions.distances >= np.median(viewing_conditions.distances, axis=1)[:, None]),
        :] = torch.nan
        aggr = torch.nanmean(probabilities, dim=1)

        # Note: aggr[:, 0] is assumed to be the default/background class
        aggr[:, 1:] = torch.nan_to_num(aggr[:, 1:], nan=0.0)
        aggr[:, 0] = torch.where(torch.isnan(aggr[:, 0]), 1 - aggr[:, 1:].sum(dim=1), aggr[:, 0])
        argmax = torch.argmax(aggr, dim=1)
        return aggr, argmax


class DistanceWeightedFuser:
    def __init__(self, class_weight=None):
        self.class_weight = class_weight

    def __call__(self, probabilities, viewing_conditions):
        probabilities = probabilities * self.class_weight if self.class_weight is not None else probabilities

        # apply angle constraint on views
        probabilities[(270 < viewing_conditions.angles) + (viewing_conditions.angles < 90), :] = torch.nan
        # TODO: cover nans?
        weight = 1 - (viewing_conditions.distances - viewing_conditions.distances.min(1)[:, None]) / (
                viewing_conditions.distances.max(1)[:, None] - viewing_conditions.distances.min(1)[:, None])
        probabilities *= weight[..., None]

        aggr = torch.nanmean(probabilities, dim=1)

        # Note: aggr[:, 0] is assumed to be the default/background class
        aggr[:, 1:] = torch.nan_to_num(aggr[:, 1:], nan=0.0)
        aggr[:, 0] = torch.where(torch.isnan(aggr[:, 0]), 1 - aggr[:, 1:].sum(dim=1), aggr[:, 0])
        argmax = torch.argmax(aggr, dim=1)
        return aggr, argmax


class AngleDistanceRangeFuser:
    def __init__(self, class_weight=None):
        self.class_weight = class_weight

    def __call__(self, probabilities, viewing_conditions):
        probabilities = probabilities * self.class_weight if self.class_weight is not None else probabilities

        # apply angle constraint on views
        # probabilities[(230 < viewing_conditions.angles) + (viewing_conditions.angles < 130), :] = torch.nan
        probabilities[(230 < viewing_conditions.angles) + (viewing_conditions.angles < 130), :] = torch.nan
        probabilities[(viewing_conditions.distances > np.median(viewing_conditions.distances, axis=1)[:, None]),
        :] = torch.nan

        aggr = torch.nanmean(probabilities, dim=1)

        # Note: aggr[:, 0] is assumed to be the default/background class
        aggr[:, 1:] = torch.nan_to_num(aggr[:, 1:], nan=0.0)
        aggr[:, 0] = torch.where(torch.isnan(aggr[:, 0]), 1 - aggr[:, 1:].sum(dim=1), aggr[:, 0])
        argmax = torch.argmax(aggr, dim=1)
        return aggr, argmax


class NaiveAngleMaxRangeFuser:
    def __init__(self, class_weight=None):
        self.class_weight = class_weight

    def __call__(self, probabilities, viewing_conditions):
        probabilities = probabilities * self.class_weight if self.class_weight is not None else probabilities

        # apply angle constraint on views
        # probabilities[(230 < viewing_conditions.angles) + (viewing_conditions.angles < 130), :] = torch.nan
        probabilities[(230 < viewing_conditions.angles) + (viewing_conditions.angles < 130), :] = torch.nan
        probabilities = torch.nan_to_num(probabilities, nan=0)
        aggr = probabilities.max(dim=1).values

        # Note: aggr[:, 0] is assumed to be the default/background class
        aggr[:, 1:] = torch.nan_to_num(aggr[:, 1:], nan=0.0)
        aggr[:, 0] = torch.where(torch.isnan(aggr[:, 0]), 1 - aggr[:, 1:].sum(dim=1), aggr[:, 0])
        argmax = torch.argmax(aggr, dim=1)
        return aggr, argmax
