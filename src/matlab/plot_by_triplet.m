function [e_avg,e_by_triplet,triplets] = plot_by_triplet( e, sequences )

% enumerate over triplets
triplets = get_triplets();

M = size( e, 1);
N = size( e, 2 );

weight = zeros( length( triplets ), N ); 
avg    = zeros( length( triplets ), N ); 

for t = 1:length( triplets )
  for i = 1 : N
    e_by_triplet{t,i} = [];
  end
end
  
tic
for t = 1:length( triplets )
  triplet = triplets{t};
  triplet_pos = strfind( sequences, triplet );
  for m = 1:M
    idx = triplet_pos{m};
    idx = idx( find( ~isinf( e( m, idx ) ) ) );
    weight( t, idx ) = weight( t, idx ) + 1;
    avg( t, idx )    = avg( t, idx ) + e( m, idx );
    for i = idx
      e_by_triplet{t,i} = [ e_by_triplet{t,i}, e(m,i) ];
    end
  end
end
toc

e_avg = avg./weight;
image( e_avg * 128 );
set(gca,'ytick',[1:length(triplets)],'yticklabel',char( triplets ) );
colormap( 1 - gray( 100 ) );

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function triplets = get_triplets();

RNA = 'ACGU';
triplets = {};
count = 0;
for i = 1:length( RNA )
  for j = 1:length( RNA )
    for k = 1:length( RNA )
      count = count + 1;
      triplets{count} = [RNA(i),RNA(j),RNA(k)];
    end
  end
end
