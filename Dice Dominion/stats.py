
import pstats
from pstats import SortKey
p = pstats.Stats('perflog.txt')

#p.strip_dirs().sort_stats(-1).print_stats()

p.sort_stats(SortKey.CUMULATIVE).print_stats(25)
#CUMULATIVE
#p.sort_stats(SortKey.CALLS).print_stats(33)
