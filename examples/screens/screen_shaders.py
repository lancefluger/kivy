fs_default = '''$HEADER$
uniform float alpha;

void main (void){
    gl_FragColor = frag_color * texture2D(texture0, tex_coord0);
}

'''


vs_default = '''$HEADER$
uniform float alpha;

void main (void) {
  frag_color = color;
  tex_coord0 = vTexCoords0;
  gl_Position = projection_mat * modelview_mat * vec4(vPosition.xy, 0.0, 1.0);
}

'''


fs_opacity = '''$HEADER$
uniform float alpha;

void main (void){
  float a = smoothstep(1.0,0.0,alpha);
  gl_FragColor = frag_color * texture2D(texture0, tex_coord0) * vec4(1.0,1.0,1.0, a);
}

'''


vs_slide_right= '''$HEADER$

uniform float alpha;
uniform vec2  size;
void main (void) {
  float a = smoothstep(1.0,0.0,alpha);
  frag_color = color;
  tex_coord0 = vTexCoords0;
  vec2 p = vPosition.xy;
  p.x += (1.0-a) * size.x;
  gl_Position = projection_mat * modelview_mat * vec4(p, 0.0, 1.0);
}

'''


