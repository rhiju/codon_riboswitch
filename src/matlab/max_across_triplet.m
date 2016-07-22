function e_max = max_across_triplet( e );


M = size( e, 1);
N = size( e, 2 );
e_max = zeros( M, N-2 );
for m = 1:M
  for n = 1:N-2
    e_max( m,n ) = max( e( m, n+[0:2]) );
  end
end
