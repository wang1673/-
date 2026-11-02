from __future__ import annotations
import logging
import numpy as np
from scipy import linalg
from numpy.lib.scimath import sqrt as scisqrt
log=logging.getLogger(__name__)

def calc_embd_statistics(embd_lst: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Calculate the mean and covariance matrix of a list of embeddings.
    """
    assert embd_lst.shape[0] >= 2, (f"FAD requires at least two embedding window frames, you have {embd_lst.shape}."
        " (This probably means that your audio is too short)")
    return np.mean(embd_lst, axis=0), np.cov(embd_lst, rowvar=False)


def calc_frechet_distance(mu1, cov1, mu2, cov2, eps=1e-6):
    """
    Adapted from: https://github.com/mseitzer/pytorch-fid/blob/master/src/pytorch_fid/fid_score.py
    
    Numpy implementation of the Frechet Distance.
    The Frechet distance between two multivariate Gaussians X_1 ~ N(mu_1, C_1)
    and X_2 ~ N(mu_2, C_2) is
            d^2 = ||mu_1 - mu_2||^2 + Tr(C_1 + C_2 - 2*sqrt(C_1*C_2)).
    Stable version by Dougal J. Sutherland.
    Params:
    -- mu1   : Numpy array containing the activations of a layer of the
            inception net (like returned by the function 'get_predictions')
            for generated samples.
    -- mu2   : The sample mean over activations, precalculated on an
            representative data set.
    -- cov1: The covariance matrix over activations for generated samples.
    -- cov2: The covariance matrix over activations, precalculated on an
            representative data set.
    Returns:
    --   : The Frechet Distance.
    """
    mu1 = np.atleast_1d(mu1)
    mu2 = np.atleast_1d(mu2)

    cov1 = np.atleast_2d(cov1)
    cov2 = np.atleast_2d(cov2)

    assert mu1.shape == mu2.shape, \
        f'Training and test mean vectors have different lengths ({mu1.shape} vs {mu2.shape})'
    assert cov1.shape == cov2.shape, \
        f'Training and test covariances have different dimensions ({cov1.shape} vs {cov2.shape})'

    diff = mu1 - mu2

    # Product might be almost singular
    # NOTE: issues with sqrtm for newer scipy versions
    # using eigenvalue method as workaround
    covmean_sqrtm, _ = linalg.sqrtm(cov1.dot(cov2), disp=False)
    
    # eigenvalue method
    D, V = linalg.eig(cov1.dot(cov2))
    covmean = (V * scisqrt(D)) @ linalg.inv(V)

    if not np.isfinite(covmean).all():
        msg = ('fid calculation produces singular product; '
            'adding %s to diagonal of cov estimates') % eps
        log.info(msg)
        offset = np.eye(cov1.shape[0]) * eps
        covmean = linalg.sqrtm((cov1 + offset).dot(cov2 + offset))

    # Numerical error might give slight imaginary component
    if np.iscomplexobj(covmean):
        if not np.allclose(np.diagonal(covmean).imag, 0, atol=1e-3):
            m = np.max(np.abs(covmean.imag))
            raise ValueError('Imaginary component {}'.format(m))
        covmean = covmean.real

    tr_covmean = np.trace(covmean)
    tr_covmean_sqrtm = np.trace(covmean_sqrtm)
    if np.iscomplexobj(tr_covmean_sqrtm):
        if np.abs(tr_covmean_sqrtm.imag) < 1e-3:
            tr_covmean_sqrtm = tr_covmean_sqrtm.real

    if not(np.iscomplexobj(tr_covmean_sqrtm)):
        delt = np.abs(tr_covmean - tr_covmean_sqrtm)
        if delt > 1e-3:
            log.warning(f'Detected high error in sqrtm calculation: {delt}')

    return (diff.dot(diff) + np.trace(cov1)
            + np.trace(cov2) - 2 * tr_covmean)

