function make_hist_plot( h_by_triplet, h_all, triplets );

r = [-12:0.2:12];

flank_bins = [38:42];
h = sum(h_all(:,flank_bins),2); 
h = h/sum(h);
plot( r, h, 'k'); hold on

seq_idx = [46 59];
colorcode = [0 0 1; 1 0 0; 0 0.5 0 ];
for n = 1:length(seq_idx);
  i = seq_idx( n );
  h = squeeze(sum(h_by_triplet( :, i, flank_bins ),3)) ;
  h = h / sum(h);
  plot( r, h, 'color', colorcode(n,:) );
end
hold off
xlim([-2 6]);
ylim([0 0.4]);
legend( ['all',triplets(seq_idx)] )
xlabel( 'log ratio of triplet exposure with and without ligand' );
ylabel( 'Frequency (normalized)' );