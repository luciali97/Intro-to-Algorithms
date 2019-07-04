# classes is a list of tuples [(g_1, b_1), (g_2, b_2), ... , (g_{n-1}, b_{n-1})] (see handout for definitions).
# T is some positive number.
# best_i is the index for which class has the best ratio
def inefficient_allocate_time(classes, T):
     time_allocated = 0
     total_benefit = 0

     while time_allocated < T:
         # Find which remaining class would be best to allocate our time to.
         best_ratio = -float('inf')
         best_i = -1
         for i, (goal, benefit) in enumerate(classes):
             if benefit/goal > best_ratio:
                 best_ratio = benefit/goal
                 best_i = i

         if best_i == -1:
             # If we run out of classes, return.
             return total_benefit

         # Allocate as much time as we can to the best class found.
         goal, benefit = classes[best_i]
         # We can't go over our limit T or over the goal limit for this class.
         time_to_allocate = min(T - time_allocated, goal)
         time_allocated += time_to_allocate
         total_benefit += benefit/goal * time_to_allocate

         # We can't allocate any more time to this class, so delete it.
         del classes[best_i]
     return total_benefit

def allocate_time(classes, T):
    time_allocated = 0
    total_benefit = 0
    d = {}
    ratios = []
    for g, b in classes:
        if b/g not in d:
            d.update({b/g: g})
            ratios.append(b/g)
        else:
            d[b/g] += g
    #print (d)
    ratios.sort(reverse = True)
    for key in ratios:
        if time_allocated < T:
            time_to_allocate = min(T - time_allocated, d[key])
            time_allocated += time_to_allocate
            total_benefit += key * time_to_allocate
        else:
            break
    return total_benefit
        
        
    
    
            
        
    
 
