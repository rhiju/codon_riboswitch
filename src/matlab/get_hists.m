function [h_by_triplet, h_all] = get_hists( e_by_triplet, r );

for i = 1:size( e_by_triplet, 1 )
  for j = 1:size( e_by_triplet, 2 )
    h_by_triplet(:,i,j) = hist( e_by_triplet{i,j}, r );
  end
end

h_all = squeeze( sum( h_by_triplet, 2 ) );

