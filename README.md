##Introduction
Prototype.py enforces Python's list operations.
It patches some sequence types and enables to write method chaining in following Scala-like style:

```python
>>> from prototype import itr
>>> itr.attach()
>>> [[1, 2], [3, 4]].flatmap(lambda x: x * 10).reduce(lambda x, y: x + y)
100
```

In addition, we can process it in parallel in a similar manner to Scala's [ParSeq](http://www.scala-lang.org/api/current/#scala.collection.parallel.ParSeq):

```python
from prototype import par
par.attach()

# We cannot use lambda because of  restrictions of multiprocessing...
def mult10(x):
    return x * 10

def accm(x, y):
    return x + y

if __name__=='__main__':
    [[1, 2], [3, 4]].par().flatmap(mult10).reduce(accm)
```

Furthermore, we can be super-happy with the library [fn.py](https://github.com/kachayev/fn.py):

```python
>>> from prototype import itr
>>> from fn import _
>>> itr.attach()
>>> [1, 2, 3, 4].map(_ * 10).reduce(_ + _)
100
```

Enjoy!

##Usage
###install
Because pip package is not provided (probably it's too danger/trivial to provide as pip).
If you want to install to your system, you can do it with:

```bash
$ git clone https://github.com/kogecoo/prototype.py.git
$ cd prototype.py
$ python setup.py install
```

###play
```python
from prototype import itr, par

def mult10(x):
    return x * 10

def even(x):
    return x % 2 == 0

if __name__=='__main__':
    mult100 = [[1,2], [3,4]].flatmap(lambda x: x * 100)

    # most of additional non-par methods return value as generator type
    print mutl100 # <generator object <genexpr> at 0xx>

    # you can convert generator to list with to_list
    print mult100.to_list()  # [100, 200, 300, 400]


    gen = (x for x in range(10))

    # This example shows both 'filter' and 'map' placed after par() process in parallel
    odd_mult10 = gen.par().filter(even).map(mult10)

    print odd_mult10  #  <parallel.parallel_collections.ParallelGen object at 0xx>

    # If you want to process in single, you can convert it to generator type with 'to_single'
    print odd_mult10.to_single()  #  <generator object <genexpr> at 0xx>

    # of course you can continue method chains after that
    print odd_mult10.to_single().map(lambda x: x/2).take(2)  # [10, 20]

```


##Requirements
* Python-Parallel-Collections >= 1.2


##Reference

### package `itr`
#### itr.attach()
Attaches a monkey patch to `list`, `tuple`, `GeneratorType`.  
Following method will be available after attaching:

* map(*function*)
* filter(*function*)
* reduce(*function[, initializer]*)
* zip()
* takewhile(*function*)
* take(*n*)
* flatmap(*function[, initializer]*)
* flatten()
* foldl(*function[, initializer]*)
  * the alias of `reduce`
* len()
  * available only for `list` and `tuple`
* to_iter()
* to_list()

#### itr.detach()
remove above features from `list`, `tuple`, `GeneratorType`.

### package `par`
#### par.attach()
Attaches a monkey patch to `list`, `tuple`, `GeneratorType`.  
You can use following methods after `some_seq.par()`:

* map(*function*)
* filter(*function*)
* reduce(*function[, initializer]*) 
* flatmap(*function[, initializer]*)
* flatten()
* fold(*function[, initializer]*)
* to_single()

Detail: `some_seq.par()` simply returns an instance of `ParallelGen`, which is used internally in [Python-Parallel-Collections](http://https://github.com/gterzian/Python-Parallel-Collections).

 Since parallel processing depends on `multiprocessing` library, function for each methods needs to be picklable.
To remove this limitation, author currently consider about using [Pathos](https://github.com/uqfoundation/pathos/issues).
Sadly, `Pathos` seems not to provide an easy way to install (e.g. pip install), so we decided that we don't depend on it.

#### par.detach()
remove above features from `list`, `tuple`, `GeneratorType`.



##Restrictions
#### supported iterable types
We supports following types.
    * ``list``
    * ``tuple``
    * ``GeneratorType``

str/unicode aren't supported.  
Other iterable objects(ex. itertools.listiterator) also aren't supported,
but you can easily use this library by converting it to generator type like:

```python
some_gen = (x for x in some_iterable)
```

### functions in parallel processing
When using parallel map/filter/etc, you need to write function at the global scope because of limitation of multiprocessing. So, sadly, you can't write a code in this way:

```python
list(range(10)).par().map(lambda x: x * 10).reduce(lambda x, y: x + y)
```

## Misc
* Feel free to pull request.
