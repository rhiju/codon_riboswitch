if ~exist( 'apt_bpp', 'var' )
  e0 = load( 'exposure_free.txt' );
  e1 = load( 'exposure_closed.txt' );
  apt_bpp = load( 'aptamer_bpp.txt' );
  sequences = textread( 'sequences.txt', '%s' );
  fprintf( 'Done reading files\n' );
end

%exposure graph
figure(1)
set(gcf, 'PaperPositionMode','auto','color','white');
N = size( e0, 1 ); e = [];
for i = 1:min(N,500)
  e = [e; e0(i,:) ];
  e = [e; e1(i,:) ];
end
clf;
image( e( 1:min( 200, size(e,1)), :) *128 )
colormap( 1 - gray(100) );
title( 'alternating off/on ligand' );
fprintf( 'Number of sequences: %d\n', N );
drawnow;

% mean exposure
figure(2)
clf;
subplot(2,1,1);
set(gcf, 'PaperPositionMode','auto','color','white');
plot( mean( e0 ),'k' ); hold on
plot( mean( e1 ),'r' );hold off
xlabel( 'Sequence position' );
ylabel( 'Base pair exposure' );
legend( 'no aptamer', 'aptamer' );

subplot(2,1,2);
M = size( apt_bpp, 1 );
plot( [1:M]/M, sort( apt_bpp(:,1) ),'k' ); hold on
plot( [1:M]/M, sort( apt_bpp(:,2) ),'r' ); hold on
cutoff = 0.8;
plot( [0 1], cutoff*[1 1],'color',[0.5 0.5 0.5] );
hold off
fprintf( 'Frac. with >%5.2f correct sec. struct: %f\n',cutoff,...
	 sum( apt_bpp(:,1)>cutoff)/length( apt_bpp(:,1) ) );
set( gca,'yscale','log' );
legend( 'no ligand', 'mimic ligand' );
xlabel( 'Fraction of constructs' );
ylabel( 'Probability of aptamer' );
drawnow;


figure(3)
%e0_trip = plot_by_triplet( e0, sequences );
%e0_trip = plot_by_triplet( e0, sequences );

e0m = max_across_triplet( e0 );
e1m = max_across_triplet( e1 );

logratio = log(e1m./(e0m+1e-6)) / log(2);
[logratio_trip,e_by_triplet,triplets] = plot_by_triplet( logratio, sequences );


figure(4)
[h_by_triplet, h_all] = get_hists( e_by_triplet, r ); 
make_hist_plot( h_by_triplet, h_all, triplets );
