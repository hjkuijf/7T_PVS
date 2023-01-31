#----------------------------------------------------------------------------------
#! Macro module ReadElastixTransformParameterFile
#/*!
# \file    ReadElastixTransformParameterFile.py
# \author  Marijn van Stralen
# \date    2014-01-10
#
# 
# */
#----------------------------------------------------------------------------------

from mevis import *
import string
import math

def init():
  ctx.field("matrix").value = idMatrix(4);

def autoRead():
  if ctx.field("autoRead").value:
    readFile();

def readFile():
  fn = ctx.field("filename").value;
  m = readParameterFile(fn);
  if m:
    ctx.field("matrix").value = m;
  else :    
    ctx.field("matrix").value = idMatrix(4);
  
def readParameterFile(fn):
  params = readTransformParameters(fn);
  #print params;
  initialFn = removeQuotes( reduce(lambda x,y:str(x)+" "+str(y),params['InitialTransformParametersFileName']));
  
  transformParams = map(float, params['TransformParameters']);
  
  M = [];
  
  if "EulerTransform" in params["Transform"][0] and int(params["FixedImageDimension"][0]) == 2: # 2D Euler
    print "Euler2D";
    center = map(float, params['CenterOfRotationPoint']);
    angle = transformParams[0];
    trans = transformParams[1:];
    M = euler2DToMatrix( angle, center, trans );
    M = homogeneousMat3ToMat4(M);
    #print M;
  elif "EulerTransform" in params["Transform"][0] and int(params["FixedImageDimension"][0]) == 3: # 3D Euler
    print "Euler3D";
    center = map(float, params['CenterOfRotationPoint']);
    angle = transformParams[0:3];
    trans = transformParams[3:];
    M = euler3DToMatrix( angle, center, trans, ctx.field("useCenter").value );
    #M = homogeneousMat3ToMat4(M);
  elif "AffineTransform" in params["Transform"][0] and int(params["FixedImageDimension"][0]) == 3: # 3D Affine
    print "Affine3D";
    center = map(float, params['CenterOfRotationPoint']);
    #M = affine3DToMatrix2( transformParams,center );
    M = affine3DToMatrix( transformParams, center, ctx.field("useCenter").value );
    #M = homogeneousMat3ToMat4(M);
  elif "AffineDTITransform" in params["Transform"][0] and int(params["FixedImageDimension"][0]) == 3: # 3D Affine
    print "AffineDTI3D";
    center = map(float, params['CenterOfRotationPoint']);
    angle = transformParams[0:3];
    skew = transformParams[3:6];
    scale = transformParams[6:9];
    trans = transformParams[9:];
    #M = affine3DToMatrix2( transformParams,center );
    M = affineDTI3DToMatrix( angle, skew, scale, trans, center, ctx.field("useCenter").value );
    #M = homogeneousMat3ToMat4(M);
        
        
  #  #print M;
  else:
    print "Transform", params["Transform"][0], "with dimension", int(params["FixedImageDimension"][0]), "not yet supported";
    return None;
  
  if initialFn == "NoInitialTransform" or not ctx.field("recursiveRead").value:
    if M:
      return M;
    else:
      return None;
  else :
    print "Read initial transform:", initialFn;
    M0 = readParameterFile(initialFn);
    if M0 and M:
      return matProd(M, M0);
      
  return None;
  
def removeQuotes(s):
  return s.replace("\"", "");

def readTransformParameters(fn):
  params = dict();
  with open(fn,'r') as f:
    txt = f.read();
    lines = txt.split("\n");
    for l in lines:
      l = l[ l.find( "(" )+1 : l.find( ")" )];
      tag = l.split(" ")[0];
      p = l.split(" ")[1:];
      #print tag, p
      if tag != "//":
        params[tag] = p;
  return params;
  
def getInitialTransformParameterFilename(paramFn):
  fn = ""
  with open(paramFn, 'r') as o:
    for line in o:
      if "InitialTransformParametersFileName" in line:
        l = line.translate(None, "\"()")
        fn = l.split()[-1]
  if MLABFileManager.exists(fn):
    return fn;
  return None;
  
def euler2DToMatrix(angle, center, translation):
  MtoOrigin = transMat( mult(center, -1) );
  MfromOrigin = transMat( center );
  Mrotate = rotation2DMatrix( angle );
  Mtranslate = transMat( translation )
  M = matProd(Mtranslate, matProd(MfromOrigin, matProd(Mrotate, MtoOrigin)));
  
  return M;

def euler3DToMatrix(angle, center, translation, useCenter=True):
  MtoOrigin = transMat( mult(center, -1) );
  MfromOrigin = transMat( center );
  Mrotate = rotation3DMatrix( angle );
  Mtranslate = transMat( translation )
  if useCenter:
    R = matProd(MfromOrigin, matProd(Mrotate, MtoOrigin));
    M = matProd(Mtranslate, matProd(MfromOrigin, matProd(Mrotate, MtoOrigin)));
    #print "Affine3D R:", R;
    #print "Affine3D T:", Mtranslate;
    #print "Affine3D M:", M;
  else :
    M = matProd(Mtranslate, Mrotate);
    #print "Affine3D R:", Mrotate;
    #print "Affine3D T:", Mtranslate;
    #print "Affine3D M:", M;
  
  return M;

def affineDTI3DToMatrix( angle, skew, scale, trans, center, useCenter ):
  MtoOrigin = transMat( mult(center, -1) );
  MfromOrigin = transMat( center );
  Mrotate = rotation3DMatrix( angle );
  Mtranslate = transMat( trans );
  Mscale = scaleMat( scale );
  Mskew = skewMat( skew );
  #M = matProd(Mtranslate, matProd(MfromOrigin, matProd(Mrotate, MtoOrigin)));
  if useCenter:
    M = matProd(Mtranslate, matProd(MfromOrigin, matProd(Mskew, matProd(Mscale, matProd(Mrotate, MtoOrigin)))));  
  else :
    M = matProd(Mtranslate, matProd(Mskew, matProd(Mscale, Mrotate)));  
  return M;
    
def affine3DToMatrix(params, center, useCenter):
  if useCenter:
    MtoOrigin = transMat( mult(center, -1) );
    MfromOrigin = transMat( center );
  
  k=0;
  Mrotate = idMatrix(4);
  for i in range(3):
    for j in range(3):
      Mrotate[i][j] = params[k];
      k += 1;
  Mtranslate = transMat( params[9:12] );
  if useCenter:
    RSS = matProd(MfromOrigin, matProd(Mrotate, MtoOrigin));
    M = matProd(Mtranslate, RSS);
    print "Affine3D RSS:", RSS;
    print "Affine3D T:", Mtranslate;
    print "Affine3D M:", M;
  else :
    M = matProd(Mtranslate, Mrotate);
    print "Affine3D RSS:", Mrotate;
    print "Affine3D T:", Mtranslate;
    print "Affine3D M:", M;
  
  return M;

def projectPointOnPlane(point, plane):
  pt = point;
  d = plane[0]*point[0] + plane[1]*point[1] + plane[2]*point[2] - plane[3];
  #print d;
  return add(point, mult(plane, d));

def computePlane(p1, p2, p3):
  p = [0,0,0,0];
  A = p1[1]*(p2[2] - p3[2]) + p2[1]*(p3[2] - p1[2]) + p3[1]*(p1[2] - p2[2]) ;
  B = p1[2]*(p2[0] - p3[0]) + p2[2]*(p3[0] - p1[0]) + p3[2]*(p1[0] - p2[0]) ;
  C = p1[0]*(p2[1] - p3[1]) + p2[0]*(p3[1] - p1[1]) + p3[0]*(p1[1] - p2[1]) ;
  D = p1[0]*(p2[1]*p3[2] - p3[1]*p2[2]) + p2[0]*(p3[1]*p1[2] - p1[1]*p3[2]) + p3[0]*(p1[1]*p2[2] - p2[1]*p1[2]);
  n = [A,B,C];
  l = length(n);
  A/=l; B/=l; C/=l; D/=l;
  return [A, B, C, D];

def cross(p1, p2):
  p = [0,0,0];
  p[0] = p1[1]*p2[2] - p2[1]*p1[2];
  p[1] = p1[2]*p2[0] - p2[2]*p1[0];
  p[2] = p1[0]*p2[1] - p2[0]*p1[1];
  return p;

def dot(p1, p2):
  p = 0;
  for i in range(len(p1)):
    p += p1[i]*p2[i];
  return p;

def subtract(p1, p2):
  p = [0,0,0];
  for i in range(3):
    p[i] = p1[i]-p2[i];
  return p;

def add(p1, p2):
  p = [0,0,0];
  for i in range(3):
    p[i] = p1[i]+p2[i];
  return p;

def mult(p1, s):
  p = zeroVec(len(p1));
  for i in range(len(p1)):
    p[i] = p1[i]*s;
  return p;

def length(p):
  return math.sqrt(dot(p,p));

def normalize(p):
  return mult( p, 1.0/length(p) );

def computePlaneIntersect(p1, p2, x0):
  c = cross(p1, p2);
  c = normalize(c);
  x = [0,0,0];
  d3 = dot(c, x0);
  d1 = p1[3];
  d2 = p2[3];
  p3 = c + [d3];
  m1 = mult(cross(p2,p3),d1);
  m2 = mult(cross(p3,p1),d2);
  m3 = mult(cross(p1,p2),d3);
  nom = add(m1, add(m2, m3));
  denom = dot( p1, cross(p2, p3) );
  x = mult(nom, 1.0/denom);
  ret = [c] + [x];
  return ret;

def rotation2DMatrix(a):
  m = idMatrix(3);
  m[0][0] = math.cos(a);
  m[0][1] = -math.sin(a);
  m[1][0] = math.sin(a);
  m[1][1] = math.cos(a);
  return m;

def rotation3DMatrix(par, computeZYX = False):
  cx = math.cos(par[0]);
  sx = math.sin(par[0]);
  cy = math.cos(par[1]);
  sy = math.sin(par[1]);
  cz = math.cos(par[2]);
  sz = math.sin(par[2]);
  
  RotationX = idMatrix(4);
  RotationX[0][0]=1;  RotationX[0][1]=0; RotationX[0][2]=0;
  RotationX[1][0]=0; RotationX[1][1]=cx;   RotationX[1][2]=-sx;
  RotationX[2][0]=0; RotationX[2][1]=sx;   RotationX[2][2]=cx;  
  
  RotationY = idMatrix(4);
  RotationY[0][0]=cy;   RotationY[0][1]=0; RotationY[0][2]=sy;
  RotationY[1][0]=0; RotationY[1][1]=1;  RotationY[1][2]=0;
  RotationY[2][0]=-sy;  RotationY[2][1]=0; RotationY[2][2]=cy;
  
  RotationZ = idMatrix(4);
  RotationZ[0][0]=cz;   RotationZ[0][1]=-sz;  RotationZ[0][2]=0;
  RotationZ[1][0]=sz;   RotationZ[1][1]=cz;   RotationZ[1][2]=0;
  RotationZ[2][0]=0; RotationZ[2][1]=0; RotationZ[2][2]=1;
  
  if computeZYX:
    rotation = matProd(RotationZ, matProd(RotationY, RotationX));
  else :
    rotation = matProd(RotationZ, matProd(RotationX, RotationY));
  
  return rotation;

def rotationMatrixFromAxisAngle(aa):
  m1 = multMat(idMatrix(3), math.cos(aa[3]));
  m2 = multMat( crossProductMatrix( aa[:3] ), math.sin( aa[3] ) );
  m3 = multMat( tensorProduct( aa[:3], aa[:3] ), (1.0 - math.cos(aa[3])) );
  r = addMat(m1, addMat(m2, m3) );
  return mat3ToMat4(r);

def mat3ToMat4(m):
  r = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1]];
  for i in range(3):
    for j in range(3):
      r[i][j] = m[i][j];
  return r;

def homogeneousMat3ToMat4(m):
  r = idMatrix(4);
  for i in range(2):
    for j in range(2):
      r[i][j] = m[i][j];
  for i in range(2):
    r[i][3] = m[i][2];
  return r;


def crossProductMatrix(v):
  return [ [0, v[2], -v[1]], [-v[2], 0, v[0]], [v[1], -v[0], 0]];

def tensorProduct(v1, v2):
  m = [];
  for i in range( len(v1) ):
    c = [];
    for j in range( len(v1) ):
      c += [v1[i]*v2[j]];
    m += [c];
  return m;

def idMatrix(n):
  m = [];
  for i in range( n ):
    c = [];
    for j in range( n ):
      if j==i:
        c += [1];
      else :
        c += [0];
    m += [c];
  return m;

def multMat(m, s):
  r = idMatrix(len(m));
  for i in range(len(m)):
    for j in range(len(m[0])):
      r[i][j] = m[i][j]*s;
  return r;

def splitMat(m):
  r = idMatrix(len(m));
  t = idMatrix(len(m));
  for i in range(len(m)-1):
    for j in range(len(m[0])-1):
      r[i][j] = m[i][j];
  for i in range(len(m)-1):
    t[i][len(m[0])-1] = m[i][len(m[0])-1];
  return (r,t);

def addMat(m1, m2):
  r = m1;
  for i in range(len(m1)):
    for j in range(len(m1[0])):
      r[i][j] = m1[i][j]+m2[i][j];
  return r;

def matProd(m1, m2):
  m=[];
  for i in range(len(m1)): #rows in m1
    c = []
    for j in range(len(m2[0])): #cols in m2
      v=0;
      for k in range(len(m1[0])): #cols in m1, #rows in m2
        v += m1[i][k]*m2[k][j];
      c += [v];
    m += [c];
  return m;

def angleBetweenVectors(v1, v2):
  return math.acos( dot(v1, v2) );

def transMat( t ):
  n = len(t)+1;
  m = idMatrix(n);
  for i in range(len(t)):
    m[i][n-1] = t[i];
  return m;

def scaleMat(s):
  n = len(s)+1;
  M = idMatrix(n);
  for i in range(len(s)):
    M[i][i] = s[i];
  return M;

# !!!! Not implemented yet
def skewMat(s):
  print "Warning: Skew matrix not implmented yet, using identity matrix! SKew parameters", s;
  n = len(s)+1;
  M = idMatrix(n);
  return M;


def rotationMatrixFromAxisAngleAndCenter(aa, c):
  #transform back to origin
  t0 = transMat( mult(c, -1) );
  r = rotationMatrixFromAxisAngle(aa);
  t1 = transMat(c);
  m = matProd(t1, matProd(r, t0));
  return m;

def matVecProd(m, v):
  mv = [ [v[0]], [v[1]], [v[2]], [1] ];
  v2 = matProd(m, mv);
  return [ v2[0][0], v2[1][0], v2[2][0] ];

def testRotation():
  t1 = [ [1,0,0], [2,0,0], [2,1,0] ];
  t2 = [ [1,0,0], [2,1,0], [1,1,-0.5] ];
  p1 = computePlane( t1[0], t1[1], t1[2] );
  print p1;
  p2 = computePlane( t2[0], t2[1], t2[2] );
  print p2;
  l = computePlaneIntersect(p1, p2, [0,0,0]);
  print l;
  a = angleBetweenVectors(p1,p2);
  print "angle: " + str(180.0/3.14*a);    
  R = rotationMatrixFromAxisAngleAndCenter( (l[0] + [ a ]), l[1] );  
  print R;
  t22 = matVecProd(R, t2[2]);
  print t22;
  
def toNumpyMat(pts):
  m = [];
  for p in pts:
    m += [p];
  return mat(m);

def zeroVec(n):
  return [0 for i in range(n)];