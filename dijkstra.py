import pygame
import numpy as np
import random
import heapq

white = (255, 255, 255)
green = (0, 255, 0)
black = (0, 0, 0)
red = (255, 0, 0)




class node:
  def __init__(self, index, x, y, color = black, radius = 20):
    self.index = index
    self.x = x
    self.y = y
    self.color = color
    self.radius = radius
    self.connections = {}
    self.links = []
  
  def draw(self, surface):
    font_obj = pygame.font.Font('freesansbold.ttf', 24)
    text_surface_obj = font_obj.render(str(self.index), True, white)
    text_rect_obj = text_surface_obj.get_rect()
    text_rect_obj.center = (self.x, self.y)

    pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)
    surface.blit(text_surface_obj, text_rect_obj)




class link:
  def __init__(self, index, from_x, from_y, to_x, to_y, length, color = black):
    self.index = index
    self.from_x = from_x
    self.from_y = from_y
    self.start = [self.from_x, self.from_y]
    self.to_x = to_x
    self.to_y = to_y
    self.end = [self.to_x, self.to_y]
    self.length = length
    self.color = color

  def draw(self, surface, start, end):
    pygame.draw.line(surface,self.color,start,end)



class dag:
  def __init__(self, num_nodes):
    self.num_nodes = num_nodes
    self.nodes = []
    self.links = []
    self.shortest_path = None
    for i in range(num_nodes):
      self.nodes.append(node(i, random.uniform(100,1400), random.uniform(100,650)))

   
    for i in range(num_nodes):
      for j in range(i + 1, num_nodes):
        if not self.nodes[j] in self.nodes[i].connections:
          if random.uniform(0,1) <= 0.65:
             new_link = link((i, j), self.nodes[i].x, self.nodes[i].y, self.nodes[j].x, self.nodes[j].y, random.uniform(0, j - i))
             self.nodes[i].links.append(new_link)
             self.nodes[i].connections.update({self.nodes[j]:new_link.length})
             self.links.append(new_link)



      
    
  def Dijkstra(self, start, end):
      for i in self.nodes:
       if(i == start): 
         setattr(i,"distance", 0)
         setattr(i, "previous", None)
       else: 
         setattr(i, "distance", float('inf'))
         setattr(i, "previous", None)
                  
      priority_queue = [(0, start)]
      

      while len(priority_queue) > 0:
       
        current_distance, current_node = heapq.heappop(priority_queue)


        if current_node == end:
          break
         
                     
        for i in current_node.connections.items():
         potential = current_distance + i[1]
         if potential < i[0].distance:
          i[0].distance = potential
          i[0].previous = current_node
          heapq.heappush(priority_queue, (i[0].distance, i[0]))


          
      s = []
      x = end
      while x != None:
        s.append(x.index)
        x = x.previous
      s.reverse()
      
     # for i in range(len(s) - 1):
      # for j in self.links:
       # if j.index == (s[i], s[i + 1]):
        #  j.color = green
         # pygame.display.flip()

      self.shortest_path = s
      return s
  
        

  def color_path(self):
   for i in range(len(self.shortest_path) - 1):
     for j in self.links:
        if j.index == (self.shortest_path[i], self.shortest_path[i + 1]):
          j.color = green
          j.draw(screen, j.start, j.end)
          pygame.display.flip()
   





        







  






pygame.init()

win_size = (1500, 750)
win_title = "Directed Acyclic Graph"
screen = pygame.display.set_mode(win_size)
pygame.display.set_caption(win_title)
screen.fill(white)


my_dag = dag(10)
sp = my_dag.Dijkstra(my_dag.nodes[0], my_dag.nodes[5])





for i in range(my_dag.num_nodes):
   my_dag.nodes[i].draw(screen)

    
for i in range(len(my_dag.links)):
   my_dag.links[i].draw(screen, my_dag.links[i].start, my_dag.links[i].end)




running  = True

while running:  
  
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
           running = False
    
    my_dag.color_path()
    pygame.display.flip()