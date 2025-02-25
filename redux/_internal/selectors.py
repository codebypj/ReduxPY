"""
    Selector related helper functions
"""
from operator import is_
from typing import Callable, TypeVar

import reactivex.operators as op
from reactivex import Observable, compose
from reactivex.subject import ReplaySubject

T1 = TypeVar('T1')
T2 = TypeVar('T2')
Mapper = Callable[[T1], T2]


def select(selector: Mapper[T1, T2]
           ) -> Callable[[Observable], Observable]:
    """ Reactive operator that applies a selector
        and shares the result across multiple subscribers

        Args:
            selector: the selector function

        Returns:
            The reactive operator
    """
    return compose(
        op.map(selector),
        op.distinct_until_changed(comparer=is_),
        op.multicast(subject=ReplaySubject(1)),
        op.ref_count(),
    )
